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

rospy.init_node('test_ur',anonymous=True)
moveit_commander.roscpp_initialize(sys.argv)

robot = moveit_commander.RobotCommander()
Scene = moveit_commander.PlanningSceneInterface()

group_name = robot.get_group_names()
current_state = robot.get_current_state()
move_group = moveit_commander.MoveGroupCommander(group_name[1])
move_group.set_max_acceleration_scaling_factor(0.01)
move_group.set_max_velocity_scaling_factor(0.1)

# move_group.set_named_target('home')
# plan = move_group.plan()
# move_group.execute(plan, wait=True)
def move_joints(move_group, goal):
    move_group.go(goal, wait=False)
    move_group.stop()
def get_joint_state(move_group, a):
    joint_state = move_group.get_current_joint_values()
    # print "->current joint state as follows(rad) :"
    # print joint_state
    print "-> current joint state as follows(degree) :"
    print np.array([joint*180./math.pi for joint in joint_state])+np.array([a,0,0,0,0,0])
    return np.array([joint*180./math.pi for joint in joint_state])+np.array([a,0,0,0,0,0])

goal = [n*math.pi/180. for n in get_joint_state(move_group, 1)]
# goal1 = [n*math.pi/180. for n in [0, -15, 0, 0, 0, 0]]
# goal2 = [n*math.pi/180. for n in [0, -20, 0, 0, 0, 0]]
# goal3 = [n*math.pi/180. for n in [60, -45, 85, -60, 0, 0]]
move_joints(move_group, goal)
get_joint_state(move_group, 1)
# move_joints(move_group, goal2)
# get_joint_state(move_group)
# move_joints(move_group, goal3)
# get_joint_state(move_group)
# for i in range (1,5):
#
#     goal = [n*math.pi/180. for n in [0, -17-i, 0, 0, 0, 0]]
#
#     move_joints(move_group, goal)
#     get_joint_state(move_group)
