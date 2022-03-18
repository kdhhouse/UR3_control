#!/usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
#



import numpy as np
import matplotlib.pyplot as plt
import rospy
from std_msgs.msg import Float32
from std_msgs.msg import Float32MultiArray
global a1
global a2
global a3
global a4
global a5
global a6

global a11
global a12
global a13
global a14
global a15
global a16

global sum
a1 = Float32()
a2 = Float32()
a3 = Float32()
a4 = Float32()
a5 = Float32()
a6 = Float32()

a11 = Float32MultiArray()
a12 = Float32MultiArray()
a13 = Float32MultiArray()
a14 = Float32MultiArray()
a15 = Float32MultiArray()
a16 = Float32MultiArray()

pub = rospy.Publisher('chatter', Float32MultiArray, queue_size=10)
rospy.init_node('listener', anonymous=True)
rate = rospy.Rate(10) # 10hz
sum = Float32MultiArray()
a11.data=np.array([])
a12.data=np.array([])
a13.data=np.array([])
a14.data=np.array([])
a15.data=np.array([])
a16.data=np.array([])


def callback1(data):
    a1.data = data.data
    a11.data = np.append(a11.data, [a1.data])
def callback2(data):
    a2.data = data.data
    a12.data = np.append(a12.data, [a2.data])
def callback3(data):
    a3.data = data.data
    a13.data = np.append(a13.data, [a3.data])
def callback4(data):
    a4.data = data.data
    a14.data = np.append(a14.data, [a4.data])
def callback5(data):
    a5.data = data.data
    a15.data = np.append(a15.data, [a5.data])
def callback6(data):
    a6.data = data.data
    a16.data = np.append(a16.data, [a6.data])
    pub = rospy.Publisher('chatter', Float32MultiArray, queue_size=10)
    rospy.init_node('listener', anonymous=True)
    sum.data = [a1.data-a11.data[0],a2.data-a12.data[0],a3.data-a13.data[0],a4.data-a14.data[0],a5.data-a15.data[0],a6.data-a16.data[0]]
    print(sum.data)
    pub.publish(sum)
    rate.sleep()


    # print(a1.data+a2.data+a3.data+a4.data+a5.data+a6.data)

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber('link_data1', Float32, callback1)
    rospy.Subscriber('link_data2', Float32, callback2)
    rospy.Subscriber('link_data3', Float32, callback3)
    rospy.Subscriber('link_data4', Float32, callback4)
    rospy.Subscriber('link_data5', Float32, callback5)
    rospy.Subscriber('link_data6', Float32, callback6)
    rospy.spin()



    # spin() simply keeps python from exiting until this node is stopped



if __name__ == '__main__':
    listener()
