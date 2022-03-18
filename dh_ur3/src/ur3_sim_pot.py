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
global joint1
global joint2

joint1 = Float32()
joint2 = Float32()

rospy.init_node('pot',anonymous=True)
moveit_commander.roscpp_initialize(sys.argv)

robot = moveit_commander.RobotCommander()
Scene = moveit_commander.PlanningSceneInterface()

group_name = robot.get_group_names()
current_state = robot.get_current_state()
move_group = moveit_commander.MoveGroupCommander(group_name[1])

rate = rospy.Rate(1)


def move_joints(move_group, goal):
    move_group.go(goal, wait=False)
def get_joint_state(move_group):
    joint_state = move_group.get_current_joint_values()
    print "->current joint state as follows(rad) :"
    print joint_state
    print "-> current joint state as follows(degree) :"
    print [joint*180./math.pi for joint in joint_state]

get_joint_state(move_group)

def callback1(data):
    joint1.data = data.data
def callback2(data):
    joint2.data = data.data
    print(joint1.data)
    goal = [n*math.pi/180. for n in [90+0.4*joint2.data, -100+0.1*joint1.data, 90, -100, -90, 0]]

    move_joints(move_group, goal)
    get_joint_state(move_group)


def listener():

    rospy.init_node('pot', anonymous=True)

    rospy.Subscriber('range_data1', Float32, callback1)
    rospy.Subscriber('range_data2', Float32, callback2)
    rospy.spin()


if __name__ == '__main__':
    listener()
