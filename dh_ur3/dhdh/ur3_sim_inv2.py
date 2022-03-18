#!/usr/bin/env python


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
move_group.set_max_acceleration_scaling_factor(0.01)
move_group.set_max_velocity_scaling_factor(0.05)

rate = rospy.Rate(10)

def move_joints(move_group, goal):
    move_group.go(goal, wait=False)
    # move_group.stop()

def get_goal_pose(move_group):
    joint_state = move_group.get_current_pose()
    return joint_state

def get_joint_state(move_group, a):
    joint_state = move_group.get_current_joint_values()
    # print "->current joint state as follows(rad) :"
    # print joint_state
    # print "-> current joint state as follows(degree) :"
    # print np.array([joint*180./math.pi for joint in joint_state])+np.array([a,0,0,0,0,0])
    return np.array([joint*180./math.pi for joint in joint_state])+np.array([a,0,0,0,0,0])


def callback(data):
    # position.data = data.data
    # rospy.init_node('test_ur', anonymous=True)
    pose_goal = get_goal_pose(move_group)
    # print([data.wrench.force.x, data.wrench.force.y, data.wrench.force.z, data.wrench.torque.x, data.wrench.torque.y, data.wrench.torque.z])
    # quat_angle = tf.transformations.euler_from_quaternion([pose_goal.pose.orientation.x, pose_goal.pose.orientation.y, pose_goal.pose.orientation.z, pose_goal.pose.orientation.w])
    # euiler_angle = [each*180./math.pi for each in quat_angle]
# print(euiler_angle)pose_goal.pose.position.z -= 0.001
    # [p, q, r] = [each*math.pi/180. for each in [0, 90, 90]]
    pub = rospy.Publisher('position_states', PoseStamped, queue_size=10)
    pub.publish(pose_goal)

    # if abs(data.wrench.force.z) > 5:
    #     # [ze] = [pose_goal.pose.position.z-data.wrench.force.z*0.02]
    #     goal = [n*math.pi/180. for n in get_joint_state(move_group, data.wrench.force.z*0.1)]
    # else:
    #     goal = [n*math.pi/180. for n in get_joint_state(move_group, 0)]
    # print(goal)
    #     # pose_goal.pose.position.z += data.wrench.force.z*0.001    # else:
    #     # [ze] = [pose_goal.pose.position.z]
    # move_joints(move_group, goal)
    # get_joint_state(move_group, 0)
    # pose_goal.pose.orientation.x = x
    # pose_goal.pose.orientation.y = y
    # pose_goal.pose.orientation.z = z
    # pose_goal.pose.orientation.w = w
    # print(pose_goal.pose.position.z)
    # print(pose_goal.pose.position)
    # print("end")
    # move_group.set_pose_target(pose_goal)
    #
    # move_group.go(wait=False)

    # move_group.stop()
    # move_group.clear_pose_targets()

def listener():

    # rospy.init_node('test_ur', anonymous=True)

    rospy.Subscriber("optoforce_0", WrenchStamped, callback)

    rospy.spin()


if __name__ == '__main__':
    listener()
