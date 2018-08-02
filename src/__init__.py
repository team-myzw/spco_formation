# -*- coding: utf-8 -*-

import rospy
import math
import numpy as np
from time import sleep
import sys, subprocess
import os.path
from std_msgs.msg import String
from std_msgs.msg import Int32
from audio_module_msg.msg import AudioSentence

TRIALNAME = "trial"

IMAGE_TOPIC = "/hsrb/head_rgbd_sensor/rgb/image_raw"
#VOCAB_TOPIC = "/spco/word_result"
VOCAB_TOPIC = "/AudioSentence"
# POSE_TOPIC = "/amcl_pose"
POSE_TOPIC = "/laser_2d_pose"

DATASET_FOLDER = "../data/"

VOCABULARY = ["キッチン","リビング","ドア前"]
