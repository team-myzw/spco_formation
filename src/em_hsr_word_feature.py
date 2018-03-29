#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __init__ import *

class GetWordFeature(object):

    def speech_callback(self, hoge):

        csv_flag = False
        #result = hoge.data
        result = hoge.sentences[0]

        for x in xrange(self.vocabulary_list_size):
            if self.vocabulary_list[x] in result:
                result = self.vocabulary_list[x]
                csv_flag = True
                break

        if csv_flag:
            fp = open(self.WORD_FOLDER + str(self.count) + ".txt",'w')
            fp.write(result+'\n')
            fp.close()
            print "[write to txt : " + result + "]"
        else :
            print "[not write to csv]\t" + result

    def recognition_callback(self, hoge):

        self.count = hoge.data

    def __init__(self):

        #rospy.Subscriber(VOCAB_TOPIC, String, self.speech_callback, queue_size=1)
        rospy.Subscriber(VOCAB_TOPIC, AudioSentence, self.speech_callback, queue_size=1)
        rospy.Subscriber("/spco/image_fin", Int32, self.recognition_callback, queue_size=1)

        self.count = 0
        self.WORD_FOLDER = DATASET_FOLDER + TRIALNAME + "/word/"
        self.vocabulary_list = ["書斎","詳細","寝室","キッチン","ドア前","真実","親子","風呂","プロ","フェイス","スイス","フォア前","黒"]
        self.vocabulary_list_size = len(self.vocabulary_list)

if __name__ == '__main__':

    rospy.init_node('GetWordFeature', anonymous=True)
    hoge = GetWordFeature()
    rospy.spin()
