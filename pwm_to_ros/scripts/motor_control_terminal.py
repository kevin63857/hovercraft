#!/usr/bin/env python
import time
import rospy
import curses
from std_msgs.msg import Float32MultiArray


def main(screen):
    pub = rospy.Publisher('motor_control', Float32MultiArray, queue_size=10)
    rospy.init_node('manual_motor_control', anonymous=True)
    rate = rospy.Rate(60)
    motors = [0.0,0.0,0.0,0.0]
    rows,colums = screen.getmaxyx()
    screen.nodelay(1) #if no input, just return
    did = ""
    while 1:
        c = screen.getch()
        if c != -1:
            screen.erase()
            if c == ord('Q'):
                raise("Quit!")
            if c == 259: #up arrow
                motors[1] += .025
                motors[2] += .025
                did = "more thrust forward"
            if c == 258: #down arrow
                motors[1] -= .025
                motors[2] -= .025
                did = "less thrust forward"
            if c == ord('y'):
                motors[0] += .025
                motors[3] += .025
                did = "more lift"
            if c == ord('h'):
                motors[0] -= .025
                motors[3] -= .025
                did = "less lift"
            if c == ord('!'):
                motors[0] += .025
                did = "motor 0 up"
            if c == ord('1'):
                motors[0] -= .025
                did = "motor 0 down"

            if c == ord('@'):
                motors[1] += .025
                did = "motor 1 up"
            if c == ord('2'):
                motors[1] -= .025
                did = "motor 1 down"

            if c == ord('#'):
                motors[2] += .025
                did = "motor 2 up"
            if c == ord('3'):
                motors[2] -= .025
                did = "motor 2 down"

            if c == ord('$'):
                motors[3] += .025
                did = "motor 3 up"
            if c == ord('4'):
                motors[3] -= .025
                did = "motor 3 down"
            if c == ord('~'):
                motors[0] += .025
                motors[1] += .025
                motors[2] += .025
                motors[3] += .025
                did = "all up"
            if c == ord('`'):
                motors[0] -= .025
                motors[1] -= .025
                motors[2] -= .025
                motors[3] -= .025
                did = "all down"
            screen.addstr(0,0,"Key: %d"%(c))
            screen.addstr(2,0,"did: %s"%(did))
        toPub=Float32MultiArray()
        toPub.data = motors
        for i in range(len(motors)):
            if motors[i] > 1:
                motors[i] = 1
            if motors[i] < 0:
                motors[i] = 0
        screen.addstr(1,0,"Motors: b:%f r:%f l:%f f:%f"%(
            motors[0]*100,
            motors[1]*100,
            motors[2]*100,
            motors[3]*100
            ))
        pub.publish(toPub)
        rate.sleep()
        # time.sleep(1/10)
        # screen.erase()
        # screen.refresh()

if __name__ == '__main__':
    curses.wrapper(main)
