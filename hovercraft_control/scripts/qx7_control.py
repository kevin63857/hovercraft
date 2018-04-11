#!/usr/bin/env python
import time
import rospy
from sensor_msgs.msg import Joy
from std_msgs.msg import Float32MultiArray

def cb(msg):
    global pub
    toPub=Float32MultiArray
    toPub.data.append(msg.axes[0]+1)/2.0)
    pub.publish(toPub)

if __name__ == '__main__':
    pub = rospy.Publisher('motor_control', Float32MultiArray, queue_size=10)
    sub = rospy.Subscriber('QX7', Joy, cb)
    rospy.init_node('QX7_Controller', anonymous=True)
    rospy.spin()
