#!/usr/bin/env python


import sys
import numpy as np
import rospy
import moveit_commander
import math
import tf
import geometry_msgs.msg

from std_msgs.msg import Float32
from std_msgs.msg import Float32MultiArray

global position

global joint1
global joint2
global joint3
global joint4
global joint5
global joint6

joint1 = float()
joint2 = float()
joint3 = float()
joint4 = float()
joint5 = float()
joint6 = float()

position = Float32MultiArray()


rospy.init_node('test_ur',anonymous=True)
moveit_commander.roscpp_initialize(sys.argv)

robot = moveit_commander.RobotCommander()
Scene = moveit_commander.PlanningSceneInterface()

group_name = robot.get_group_names()
current_state = robot.get_current_state()
move_group = moveit_commander.MoveGroupCommander(group_name[1])

rate = rospy.Rate(1)


def move_joints(move_group, goal):
    move_group.go(goal, wait=False)
    move_group.stop()
def get_joint_state(move_group):
    joint_state = move_group.get_current_joint_values()
    print "->current joint state as follows(rad) :"
    print joint_state
    print "-> current joint state as follows(degree) :"
    print [joint*180./math.pi for joint in joint_state]



def callback(data):
    position.data = data.data
    rospy.init_node('test_ur', anonymous=True)
    print(move_group.get_current_joint_values()[0]*180/math.pi)
    if abs(position.data[0]) > 0.1:
        goal = [n*math.pi/180. for n in [move_group.get_current_joint_values()[0]*180/math.pi+position.data[0]*50, -120, 90, -100, -90, 0]]
        print(position.data[0])
    else:
        goal = [n*math.pi/180. for n in [move_group.get_current_joint_values()[0]*180/math.pi, -120, 90, -100, -90, 0]]
        print(position.data[0])
    # [joint1, joint2, joint3, joint4, joint5, joint6] = goal

    move_joints(move_group, goal)
    # get_joint_state(move_group)


def listener():

    rospy.init_node('test_ur', anonymous=True)

    rospy.Subscriber('range', Float32MultiArray, callback)

    rospy.spin()


if __name__ == '__main__':
    listener()
