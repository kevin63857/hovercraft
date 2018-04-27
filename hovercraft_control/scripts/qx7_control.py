#!/usr/bin/env python
import time
import rospy
from sensor_msgs.msg import Joy
from std_msgs.msg import Float32MultiArray
def bound_on_range(val):
    val=val if val<=1 else 1
    val=val if val>=0 else 0
    return val

def cb(msg):
    global pub
    toPub=Float32MultiArray()
    #toPub.data=[.15,.15,.15,.15]
    #pub.publish(toPub)
    #return
    lift=(msg.axes[0]+1)/2 #0 to 1
    yaw=(msg.axes[3]/2)#-.5 to .5
    thrust=(msg.axes[1] if msg.axes[1]>0 else 0)#-1 to 1, but ignore negatives
    roll=(msg.axes[2]/2)#-.5 to .5

    #set motor values
    front_lift=bound_on_range(lift+yaw)
    back_lift=bound_on_range(lift-yaw)
    left_thrust=bound_on_range(thrust+roll)
    right_thrust=bound_on_range(thrust-roll)

    #left thrust is 2
    #right thrust is 1
    #front lift is 3
    #back lift is 0
    toPub.data=[back_lift,right_thrust,left_thrust,front_lift]
    pub.publish(toPub)

if __name__ == '__main__':
    pub = rospy.Publisher('motor_control', Float32MultiArray, queue_size=10)
    sub = rospy.Subscriber('QX7', Joy, cb)
    rospy.init_node('QX7_Controller', anonymous=True)
    rospy.spin()
