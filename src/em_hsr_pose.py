#! /usr/bin/env python

from __init__ import *

from geometry_msgs.msg import Point
from geometry_msgs.msg import PoseWithCovarianceStamped
# from geometry_msgs.msg import PoseStamped

p = subprocess.Popen("rm -rf " + DATASET_FOLDER + TRIALNAME, shell=True)
sleep(1)
p = subprocess.Popen("mkdir -p " + DATASET_FOLDER + TRIALNAME + "/image/", shell=True)
p = subprocess.Popen("mkdir -p " + DATASET_FOLDER + TRIALNAME + "/position_data/", shell=True)
p = subprocess.Popen("mkdir -p " + DATASET_FOLDER + TRIALNAME + "/word/", shell=True)
print "mkdir "+ DATASET_FOLDER + TRIALNAME

class GetPose(object):

    def pose_callback(self, hoge):

        if self.flag == False:
            print "Waiting for image topic"
            return
        self.count += 1

        pose = hoge.pose.pose.position
        orientation = hoge.pose.pose.orientation

        print pose
        print orientation

        sin = 2 * orientation.w * orientation.z
        cos = orientation.w * orientation.w - orientation.z * orientation.z

        self.pub_to_pose.publish(self.count)
        fp = open(self.POSE_FOLDER + str(self.count) + ".txt",'w')
        fp.write(str(pose.x) + " " + str(pose.y) + "\n" + str(sin) + " " + str(cos))
        fp.close()

    def flag_callback(self, hoge):

        self.flag = True

    def __init__(self):

        self.pub_to_pose = rospy.Publisher("/spco/image_fin", Int32, queue_size=1)
        rospy.Subscriber(POSE_TOPIC, PoseWithCovarianceStamped, self.pose_callback, queue_size=1)
        rospy.Subscriber("/spco/flag", String, self.flag_callback, queue_size=1)

        self.POSE_FOLDER = DATASET_FOLDER + TRIALNAME + "/position_data/"
        self.count = 0
        self.flag = False

if __name__ == '__main__':

    rospy.init_node('GetPose', anonymous=True)
    hoge = GetPose()
    rospy.spin()
