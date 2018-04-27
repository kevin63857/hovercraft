#!/usr/bin/env python
import pygame
import time
import rospy
from sensor_msgs.msg import Joy

if __name__ == '__main__':
    pygame.display.init()
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    qx7=None
    for i in joysticks:
        if 'FrSky' in i.get_name():
            qx7=i
    if qx7 is None:
        print "Could not find qx7, exiting"
        exit()
    qx7.init()
    pub = rospy.Publisher('QX7', Joy, queue_size=10)
    rospy.init_node('QX7_Pub', anonymous=True)
    rate = rospy.Rate(100) # 10hz
    has_recieved_data=False
    while not rospy.is_shutdown():
        msg=Joy()
        pygame.event.pump()
        print "Axes:"
        for i in range(0,qx7.get_numaxes()):
            print i,qx7.get_axis(i)
            if qx7.get_axis(i)!=0:
                has_recieved_data=True
            msg.axes.append(qx7.get_axis(i))
        print "Buttons:"
        for i in range(0,qx7.get_numbuttons()):
            print i,qx7.get_button(i)
            msg.buttons.append(qx7.get_button(i))
        print ""
        if not has_recieved_data:
            msg.axes[0]=-1
        msg.header.stamp=rospy.Time.now()
        pub.publish(msg)
        rate.sleep()
