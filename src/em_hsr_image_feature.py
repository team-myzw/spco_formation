#! /usr/bin/env python

from __init__ import *

import glob
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


class GetImageFeature(object):

    def recognition_callback(self, hoge):

        image_name = self.IMAGE_FOLDER + str(hoge.data) + ".jpg"

        cv2.imwrite(image_name, self.frame)
        print "save new image as " + image_name

    def image_callback(self, image):

        bridge = CvBridge()
        try:
            self.frame = bridge.imgmsg_to_cv2(image, "bgr8")
        except CvBridgeError, e:
            print e

        if self.count < 10:
            self.flag = True
            self.pub_flag.publish("hoge")
            self.count += 1

    def __init__(self):

        self.pub_flag = rospy.Publisher("/spco/flag", String, queue_size=1)
        rospy.Subscriber(IMAGE_TOPIC, Image, self.image_callback, queue_size=1)
        rospy.Subscriber("/spco/image_fin", Int32, self.recognition_callback, queue_size=1)
        self.IMAGE_FOLDER = DATASET_FOLDER + TRIALNAME + "/image/"

        self.count = 0
        self.flag = False

if __name__ == '__main__':

    rospy.init_node('GetImageFeature', anonymous=True)
    hoge = GetImageFeature()
    rospy.spin()
