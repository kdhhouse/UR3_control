#!/usr/bin/env python



import numpy as np
import matplotlib.pyplot as plt
import rospy
from std_msgs.msg import Float32
from std_msgs.msg import Float32MultiArray

global strain1
global strain2

global x
global y
global z
global r
global p
global w

global straintoforce
global straintorange

straintoforce = np.array([[-3266.37269700000, 2978.20261600000, -1372.28141800000, -1224.91041300000, 1913.49821000000, -1472.75915500000],
                            [2716.63223000000, -1147.51836600000, -3069.74342800000, 3025.69752300000, 273.925290100000, -1998.78280700000],
                            [2950.14228600000, 5957.57114800000, 4676.88587100000, 3823.35673000000, 4971.51815500000, 3656.91857300000],
                            [-312.904664000000, 230.563792600000, 425.567663100000, -423.742859400000, -112.279299600000, 217.970144700000],
                            [-603.737166300000, 481.984348300000, -107.195782800000, -115.027643000000, 299.849262600000, -285.919972000000],
                            [21.1804400700000, -20.0416492800000, 39.4430793700000, -28.4921765300000, 16.5277697300000, -12.9746592700000]])*0.0001
straintorange = np.array([[-53.5722416000000, 67.3972796300000, -29.8124660900000, -40.0830315100000, 44.6479064900000, -16.9416514500000],

[108.314825600000, -45.3214324900000, -107.24270510000, 114.552121500000, -9.5877527030000, -52.1198697600000],
[-1.19190766300000, 13.5551562400000, 6.05210983600000, 5.74806641400000, 9.99600026000000, 4.28803956400000],
[-117.416999400000, 83.3030798000000, 144.554383000000, -169.14827150000, -31.119644330000, 43.3004368000000],
[-149.146321600000, 128.570861000000, 13.1266790200000, -35.077607910000, 78.2283932800000, -55.6400766500000],
[54.0531904600000, -81.9743391800000, 210.549024500000, -186.22158420000, 67.2015907200000, -54.4114608600000]])*0.0001


pub1 = rospy.Publisher('force', Float32MultiArray, queue_size=10)
pub2 = rospy.Publisher('range', Float32MultiArray, queue_size=10)

pub21 = rospy.Publisher('rangex', Float32, queue_size=10)
pub22 = rospy.Publisher('rangey', Float32, queue_size=10)
pub23 = rospy.Publisher('rangez', Float32, queue_size=10)
pub24 = rospy.Publisher('ranger', Float32, queue_size=10)
pub25 = rospy.Publisher('rangep', Float32, queue_size=10)
pub26 = rospy.Publisher('rangew', Float32, queue_size=10)

strain1 = Float32MultiArray()
strain2 = Float32MultiArray()
x=Float32()
y=Float32()
z=Float32()
r=Float32()
p=Float32()
w=Float32()

rospy.init_node('matrix', anonymous=True)
rate = rospy.Rate(10) # 10hz


def callback(data):
    strain1.data = straintoforce.dot(np.transpose(np.array([data.data])))
    strain2.data = straintorange.dot(np.transpose(np.array([data.data])))
    x.data = straintorange.dot(np.transpose(np.array([data.data])))[0]
    y.data = straintorange.dot(np.transpose(np.array([data.data])))[1]
    z.data = straintorange.dot(np.transpose(np.array([data.data])))[2]
    r.data = straintorange.dot(np.transpose(np.array([data.data])))[3]
    p.data = straintorange.dot(np.transpose(np.array([data.data])))[4]
    w.data = straintorange.dot(np.transpose(np.array([data.data])))[5]
    rospy.init_node('matrix', anonymous=True)
    # rospy.loginfo(strain1.data)
    rospy.loginfo(strain2.data)
    pub1.publish(strain1)
    pub2.publish(strain2)
    pub21.publish(x)
    pub22.publish(y)
    pub23.publish(z)
    pub24.publish(r)
    pub25.publish(p)
    pub26.publish(w)
    rate.sleep()

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('matrix', anonymous=True)

    rospy.Subscriber('chatter', Float32MultiArray, callback)

    rospy.spin()


if __name__ == '__main__':
    listener()
