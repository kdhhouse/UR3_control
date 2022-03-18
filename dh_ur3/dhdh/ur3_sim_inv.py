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
global p
global q
global r
global xe
global ye
global ze
p = float()
q = float()
r = float()

position = Float32MultiArray()

rospy.init_node('test_ur',anonymous=True)
moveit_commander.roscpp_initialize(sys.argv)

robot = moveit_commander.RobotCommander()
Scene = moveit_commander.PlanningSceneInterface()

group_name = robot.get_group_names()
current_state = robot.get_current_state()
move_group = moveit_commander.MoveGroupCommander(group_name[1])
pose_goal = geometry_msgs.msg.Pose()
move_group.set_max_acceleration_scaling_factor(0.1)
move_group.set_max_velocity_scaling_factor(0.1)

def get_goal_pose(move_group):
    joint_state = move_group.get_current_pose()
    return joint_state

pose_goal = get_goal_pose(move_group)
print(pose_goal)
quat_angle = tf.transformations.euler_from_quaternion([pose_goal.pose.orientation.x, pose_goal.pose.orientation.y, pose_goal.pose.orientation.z, pose_goal.pose.orientation.w])
euiler_angle = [each*180./math.pi for each in quat_angle]
# pose_goal.pose.position.x = 0.15
pose_goal.pose.position.y -= 0.0
pose_goal.pose.position.z -= 0.05
move_group.set_pose_target(pose_goal)
move_group.go(wait=False)
# move_group.stop()
move_group.clear_pose_targets()
