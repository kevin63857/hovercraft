#!/usr/bin/env python
import time
import rospy
import socket
from threading import Thread
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
    thrust=(msg.axes[2] if msg.axes[2]>0 else 0)#-1 to 1, but ignore negatives
    roll=(msg.axes[1]/2)#-.5 to .5

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

dat=48
def pub_thread(pub):
    global dat
    rate=rospy.Rate(60)
    #Flat hand is 2
    #Peace is 3
    #Fist is 4
    lastTime=time.time()
    while not rospy.is_shutdown():
        if dat==0:#Nothing
            if time.time()-lastTime>1:
                toPub=Float32MultiArray()
                toPub.data=[0,0,0,0]
                pub.publish(toPub)
            continue
        if dat==2:#30%
            toPub=Float32MultiArray()
            toPub.data=[.8,.3,.3,.8]
            pub.publish(toPub)
            lastTime=time.time()
        if dat==3:#FULL THRUST
            toPub=Float32MultiArray()
            toPub.data=[1,1,1,1]
            pub.publish(toPub)
            lastTime=time.time()
        if dat==4:#Just hover
            toPub=Float32MultiArray()
            toPub.data=[.8,0,0,.8]
            pub.publish(toPub)
            lastTime=time.time()
        rate.sleep()

if __name__ == '__main__':
    pub = rospy.Publisher('motor_control', Float32MultiArray, queue_size=10)
    rospy.init_node('Gesture_controller', anonymous=True)
    serversocket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
    #bind the socket to a public host,
    # and a well-known port
    serversocket.bind(('', 63857))
    #become a server socket
    serversocket.listen(5)
    thr = Thread(target=pub_thread,args=(pub,))
    thr.start()
    while True:
        (clientsocket, address) = serversocket.accept()
        print "We got a connection"
        try:
            while True:
                incoming=clientsocket.recv(1)
                dat=ord(incoming)-48
                print dat
        except:
            print "Connection Failed"
            continue;
