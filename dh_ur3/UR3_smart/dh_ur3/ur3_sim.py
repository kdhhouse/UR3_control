import sys
import rospy
import moveit_commander
import math
import tf
import geometry_msgs.msg


rospy.init_node('test_ur',anonymous=True)
moveit_commander.roscpp_initialize(sys.argv)

robot = moveit_commander.RobotCommander()
Scene = moveit_commander.PlanningSceneInterface()

group_name = robot.get_group_names()
current_state = robot.get_current_state()
move_group = moveit_commander.MoveGroupCommander(group_name[1])



move_group.set_named_target('home')
plan = move_group.plan()
move_group.execute(plan, wait=True)
def move_joints(move_group, goal):
    move_group.go(goal, wait=True)
    move_group.stop()
def get_joint_state(move_group):
    joint_state = move_group.get_current_joint_values()
    print "->current joint state as follows(rad) :"
    print joint_state
    print "-> current joint state as follows(degree) :"
    print [joint*180./math.pi for joint in joint_state]

get_joint_state(move_group)

goal = [n*math.pi/180. for n in [90., -120., 90., -100., -90., 0.]]

move_joints(move_group, goal)
get_joint_state(move_group)
