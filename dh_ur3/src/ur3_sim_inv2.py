#!/usr/bin/env python

import time
import sys
import numpy as np
import rospy
import moveit_commander
import math
import tf
import geometry_msgs.msg
from std_msgs.msg import String
from geometry_msgs.msg import WrenchStamped
from geometry_msgs.msg import PoseStamped

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
pos_pub = rospy.Publisher('position_states', PoseStamped, queue_size=10)

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

rate = rospy.Rate(10)

def move_joints(move_group, goal):
    move_group.go(goal, wait=False)
    # move_group.stop()

def get_goal_pose(move_group):
    joint_state = move_group.get_current_pose()
    return joint_state

def get_joint_state(move_group, a, b):
    joint_state = move_group.get_current_joint_values()
    # print "->current joint state as follows(rad) :"
    # print joint_state
    # print "-> current joint state as follows(degree) :"
    # print np.array([joint*180./math.pi for joint in joint_state])+np.array([a,0,0,0,0,0])
    return np.array([joint*180./math.pi for joint in joint_state])*np.array([0,0,1,1,1,1])+np.array([a,b,0,0,0,0])


def callback1(data):

    pose_goal = get_goal_pose(move_group)

    pub = rospy.Publisher('position_states', PoseStamped, queue_size=10)
    pub.publish(pose_goal)
    quat_angle = tf.transformations.euler_from_quaternion([pose_goal.pose.orientation.x, pose_goal.pose.orientation.y, pose_goal.pose.orientation.z, pose_goal.pose.orientation.w])
    euiler_angle = [each*180./math.pi for each in quat_angle]
    pose_goal.pose.position.x = pose_goal.pose.position.x+data.wrench.force.x*0.005
    pose_goal.pose.position.y = pose_goal.pose.position.y+data.wrench.force.y*0.005
    pose_goal.pose.position.z = pose_goal.pose.position.z+data.wrench.force.z*0.005
    move_group.set_pose_target(pose_goal)
    move_group.go(wait=False)
    move_group.clear_pose_targets()


def callback2(data):

    pose_goal = get_goal_pose(move_group)

    pub = rospy.Publisher('position_states', PoseStamped, queue_size=10)
    pub.publish(pose_goal)


        # [ze] = [pose_goal.pose.position.z-data.wrench.force.z*0.02]
    goal = [n*math.pi/180. for n in get_joint_state(move_group, data.data[0]*0.2, -60+0.2*data.data[1])]
    move_joints(move_group, goal)
    # time.sleep(0.1)


def listener():

    rospy.Subscriber("optoforce_0", WrenchStamped, callback1)
    # time.sleep(1)
    # rospy.Subscriber("range_data", Float32MultiArray, callback1)

    rospy.spin()


if __name__ == '__main__':
    listener()
