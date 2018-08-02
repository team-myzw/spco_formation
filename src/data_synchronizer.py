#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __init__ import *

import os
import rospy
import message_filters
from sensor_msgs.msg import Image, CameraInfo
from geometry_msgs.msg import PoseWithCovarianceStamped
from audio_module_msg.msg import AudioSentence

import cv2
from cv_bridge import CvBridge, CvBridgeError

p = subprocess.Popen("rm -rf " + DATASET_FOLDER + TRIALNAME, shell=True)
sleep(1)
p = subprocess.Popen("mkdir -p " + DATASET_FOLDER + TRIALNAME + "/image/", shell=True)
p = subprocess.Popen("mkdir -p " + DATASET_FOLDER + TRIALNAME + "/position_data/", shell=True)
p = subprocess.Popen("mkdir -p " + DATASET_FOLDER + TRIALNAME + "/word/", shell=True)
print "mkdir "+ DATASET_FOLDER + TRIALNAME

class SynchronizeSaver(object):
    def __init__(self, aollow_time_delay, pose_folder, image_folder, word_folder, debug_md=False): 
        # save directories
        self.POSE_FOLDER = pose_folder
        self.IMAGE_FOLDER = image_folder
        self.WORD_FOLDER = word_folder
        for dirpath in [self.POSE_FOLDER, self.IMAGE_FOLDER, self.WORD_FOLDER]:
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)

        # subscribe settings
        laser2d_sub = message_filters.Subscriber("/laser_2d_pose", PoseWithCovarianceStamped)
        image_sub = message_filters.Subscriber("/hsrb/head_rgbd_sensor/rgb/image_raw", Image)
        audio_sub = message_filters.Subscriber("/AudioSentence", AudioSentence)

        self.aollow_time_delay = aollow_time_delay # sec
        ats = message_filters.ApproximateTimeSynchronizer([image_sub, laser2d_sub, audio_sub], 
                                                            1, self.aollow_time_delay)
        ats.registerCallback(self.approximate_synccallback)

        # other paramaters
        self.count = 0
        self.debug_md = debug_md

        #seting_word_info
        self.vocabulary_list = VOCABULARY
        self.vocabulary_list_size = len(self.vocabulary_list)
  

    def approximate_synccallback(self, image, laser2d, audio):
        self.count += 1

        if self.debug_md:
            print ("count : {0}. allow_delay_time : {1}[s]".format(self.count, self.aollow_time_delay))
            print (audio.header)
            print (image.header)
            print (laser2d.header)
            print ("-"*10)

        # save pose info
        pose = laser2d.pose.pose.position
        orientation = laser2d.pose.pose.orientation
        sin = 2 * orientation.w * orientation.z
        cos = orientation.w * orientation.w - orientation.z * orientation.z
        with open(os.path.join(self.POSE_FOLDER, "{0}.txt".format(self.count)),'w') as fp:
            fp.write(str(pose.x) + " " + str(pose.y) + "\n" + str(sin) + " " + str(cos))

        # save image info
        bridge = CvBridge()
        try:
            cv_image_frame = bridge.imgmsg_to_cv2(image, "bgr8")
        except CvBridgeError, e:
            print (e)     
        image_name = os.path.join(self.IMAGE_FOLDER, "{0}.jpg".format(self.count))
        cv2.imwrite(image_name, cv_image_frame)

        # save word info
        result = audio.sentences[0]
        for x in xrange(self.vocabulary_list_size):
            if self.vocabulary_list[x] in result:
                result = self.vocabulary_list[x]
                with open(os.path.join(self.WORD_FOLDER, "{0}.txt".format(self.count)),'w') as fp:
                    fp.write(result+"\n")
                break

if __name__ == "__main__":
    rospy.init_node("synchronizer")
    pose_f = DATASET_FOLDER + TRIALNAME + "/position_data/"
    image_f = DATASET_FOLDER + TRIALNAME + "/image/"
    word_f = DATASET_FOLDER + TRIALNAME + "/word/"
    saver = SynchronizeSaver(10, pose_f, image_f, word_f, debug_md=True)
    print ("synchronizer running..")
    rospy.spin()
