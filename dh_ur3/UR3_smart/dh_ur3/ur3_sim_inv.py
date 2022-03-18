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
pose_goal = geometry_msgs.msg.Pose()

def get_goal_pose(move_groupo):
    joint_state = move_group.get_current_pose()
    return joint_state

pose_goal = get_goal_pose(move_group)
print(pose_goal)

quat_angle = tf.transformations.euler_from_quaternion([pose_goal.pose.orientation.x, pose_goal.pose.orientation.y, pose_goal.pose.orientation.z, pose_goal.pose.orientation.w])
euiler_angle = [each*180./math.pi for each in quat_angle]
print(euiler_angle)
[p, q, r] = [each*math.pi/180. for each in [0., 90., 90.]]
[xe, ye, ze] = [0.2, 0.2, 0.3]
x, y, z, w = tf.transformations.quaternion_from_euler(p, q, r)

print([x, y, z, w])
pose_goal.pose.position.x = xe
pose_goal.pose.position.y = ye
pose_goal.pose.position.z = ze
pose_goal.pose.orientation.x = x
pose_goal.pose.orientation.y = y
pose_goal.pose.orientation.z = z
pose_goal.pose.orientation.w = w

move_group.set_pose_target(pose_goal)

plan = move_group.go(wait=True)
move_group.stop()
print(pose_goal)
move_group.clear_pose_targets()
