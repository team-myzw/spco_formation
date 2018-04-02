#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import actionlib
from actionlib_msgs.msg import GoalStatus
from geometry_msgs.msg import Point, PoseStamped, Quaternion
from std_msgs.msg import Bool
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import rospy
import tf.transformations

#actionでゴールを与える
#def MoveCallback(msg):
#    goal_x = msg.x
#    goal_y = msg.y
#    rad = math.atan2(goal_y,goal_x)
#    print "Goal Subscribe\n"
#    print "Move to (" + str(goal_x) + " , " + str(goal_y) + " , " + str(rad*180/math.pi) + ")"

#    cli = actionlib.SimpleActionClient('/move_base', MoveBaseAction)
#    cli.wait_for_server()
#    pose = PoseStamped()
#    pose.header.stamp = rospy.Time.now()
#    pose.header.frame_id = "base_link"
#    pose.pose.position = Point(goal_x, goal_y, 0)
#    quat = tf.transformations.quaternion_from_euler(0, 0, rad)
#    pose.pose.orientation = Quaternion(*quat)

#    goal = MoveBaseGoal()
#    goal.target_pose = pose

#    cli.send_goal(goal)
#    cli.wait_for_result()

#    action_state = cli.get_state()
#    if action_state == GoalStatus.SUCCEEDED:
#        rospy.loginfo("Navigation Succeeded.")


def MoveCallback(msg):
    print "Goal Subscribe\n"
    print "Move to (" + str(msg.pose.position.x) + " , " + str(msg.pose.position.y) + " , " + str(rad*180/math.pi) + ")"

    cli = actionlib.SimpleActionClient('/move_base', MoveBaseAction)
    cli.wait_for_server()
    pose = msg
    pose.header.stamp = rospy.Time.now()
    pose.header.frame_id = "base_link"

    goal = MoveBaseGoal()
    goal.target_pose = pose

    cli.send_goal(goal)
    cli.wait_for_result()

    action_state = cli.get_state()
    if action_state == GoalStatus.SUCCEEDED:
        rospy.loginfo("Navigation Succeeded.")

def TestCallback(msg):
    goal_x = 1
    goal_y = 0
    goal_yaw = 0
    print "Goal Subscribe"
    print "Move to (" + str(goal_x) + " , " + str(goal_y) + " , " + str(goal_yaw) + ")\n"

    cli = actionlib.SimpleActionClient('/move_base', MoveBaseAction)
    cli.wait_for_server()
    pose = PoseStamped()
    pose.header.stamp = rospy.Time.now()
    pose.header.frame_id = "base_link"
    pose.pose.position = Point(goal_x, goal_y, 0)
    quat = tf.transformations.quaternion_from_euler(0, 0, goal_yaw)
    pose.pose.orientation = Quaternion(*quat)

    goal = MoveBaseGoal()
    goal.target_pose = pose

    cli.send_goal(goal)
    cli.wait_for_result()

    action_state = cli.get_state()
    if action_state == GoalStatus.SUCCEEDED:
        rospy.loginfo("Navigation Succeeded.")

def run():
    rospy.init_node('em_path_plan', anonymous=True)
    #rospy.Subscriber("/spco/place_pub",Point,MoveCallback)
    rospy.Subscriber("/spco/place_pub",PoseStamped,MoveCallback)
    rospy.Subscriber("/test",Bool,TestCallback)
    rospy.spin()

if __name__ == '__main__':
    run()

