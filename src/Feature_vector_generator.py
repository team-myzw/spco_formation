#!/usr/bin/env python
#data 2016 June
#author Satoshi Ishibushi
#Create feature_vector and feature rank directory
import numpy as np
import os
import sys
import argparse
import glob
import time
import caffe
import re

LAYER="prob"
def main(argv):
    pycaffe_dir = os.path.dirname(__file__)
    pycaffe_dir = os.path.expanduser("~/caffe")

    parser = argparse.ArgumentParser()
    # Required arguments: input and output files.
    parser.add_argument(
        "input_directory",
        help="Input training directory."
    )
    # Optional arguments.
    parser.add_argument(
        "--model_def",
        default=os.path.join(pycaffe_dir,
                "models/bvlc_reference_caffenet/deploy.prototxt"),
        help="Model definition file."
    )
    parser.add_argument(
        "--pretrained_model",
        default=os.path.join(pycaffe_dir,
                "models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel"),
        help="Trained model weights file."
    )
    parser.add_argument(
        "--gpu",
        action='store_true',
        help="Switch for gpu computation."
    )
    parser.add_argument(
        "--center_only",
        action='store_true',
        help="Switch for prediction from center crop alone instead of " +
             "averaging predictions across crops (default)."
    )
    parser.add_argument(
        "--images_dim",
        default='480,640',
        help="Canonical 'height,width' dimensions of input images."
    )
    parser.add_argument(
        "--mean_file",
        default=os.path.join(pycaffe_dir,
                             'python/caffe/imagenet/ilsvrc_2012_mean.npy'),
        help="Data set image mean of [Channels x Height x Width] dimensions " +
             "(numpy array). Set to '' for no mean subtraction."
    )
    parser.add_argument(
        "--input_scale",
        type=float,
        help="Multiply input features by this scale to finish preprocessing."
    )
    parser.add_argument(
        "--channel_swap",
        default='2,1,0',
        help="Order to permute input channels. The default converts " +
             "RGB -> BGR since BGR is the Caffe default by way of OpenCV."
    )
    parser.add_argument(
        "--ext",
        default='jpg',
        help="Image file extension to take as input when a directory " +
             "is given as the input file."
    )
    args = parser.parse_args()

    image_dims = [int(s) for s in args.images_dim.split(',')]

    mean, channel_swap = None, None
    if args.mean_file:
        mean = np.load(args.mean_file)
    if args.channel_swap:
        channel_swap = [int(s) for s in args.channel_swap.split(',')]

    if args.gpu:
        caffe.set_mode_gpu()
        print("GPU mode")
    else:
        caffe.set_mode_cpu()
        print("CPU mode")

    # Make classifier.
    classifier = caffe.Classifier(args.model_def, args.pretrained_model,
            image_dims=image_dims, mean=mean,
            input_scale=args.input_scale, raw_scale=255.0,
            channel_swap=channel_swap)

    # Load numpy array (.npy), directory glob (*.jpg), or image file.
    all_file=glob.glob(args.input_directory+"/image/*."+args.ext)
    # print all_file
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    all_file.sort(key=alphanum_key)
    try:
        os.mkdir(args.input_directory+"/feature_vector")
        os.mkdir(args.input_directory+"/feature_rank")
    except:
        pass
    categories = np.loadtxt(pycaffe_dir+"/data/ilsvrc12/synset_words.txt", str, delimiter="\t")
    start = time.time()
    i = 1
    for f in all_file:
        print ("Loading file: %s" % f)

        inputs = [caffe.io.load_image(f)]
        scores = classifier.predict(inputs, not args.center_only)
        prediction = zip(scores[0].tolist(), categories)

        file_name,ext=os.path.splitext(os.path.split(f)[1])
        
        feat=feat = classifier.blobs[LAYER].data
        feat =np.average(feat,axis=0)
        fw=open(args.input_directory+"/feature_vector/"+str(i)+".txt",'w')
        # print feat
        # for rank, (score, name) in enumerate(feat, start=0):
        for rank in xrange(len(feat)):
            fw.write('%d %d\n' % (rank, feat[rank]*100))
        fw.close()
        prediction.sort(cmp=lambda x, y: cmp(x[0], y[0]), reverse=True)

        fw=open(args.input_directory+"/feature_rank/"+str(i)+".txt",'w')
        for rank, (score, name) in enumerate(prediction[:1000], start=1):
            fw.write('#%d | %s | %4.1f%% \n' % (rank, name, score * 100))
        fw.close()
        i += 1

    print("Done in %.2f s." % (time.time() - start))



if __name__ == '__main__':
    main(sys.argv)
