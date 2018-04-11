#!/usr/bin/env python

import sys
import time
import rospy
from std_msgs.msg import Float32MultiArray
import Adafruit_PCA9685
data_received_time=0
data=None
def set_servo_pulse_all(pwm, pulse):
    for channel in range(16):
        set_servo_pulse(pwm,channel,pulse)

def set_servo_pulse(pwm, channel, pulse): #pulse is in microsecond
    pulse_length = 1000000 / 60 / 4096
    pulse /= pulse_length
    pwm.set_pwm(channel, 0, int(pulse))

def calibrate(pwm,low,high):
    print("setting high")
    set_servo_pulse_all(pwm,high)
    raw_input("connect battery now, press enter when esc has booted")
    print("setting low")
    set_servo_pulse_all(pwm,low)
    print("set low, should be done")

def cb(msg):
    global data_received_time, data
    data=msg.data
    data_received_time=time.time()

def main():
    low = 1000
    high = 2000
    SCALAR= 65
    pwm = Adafruit_PCA9685.PCA9685()
    pwm.set_pwm_freq(60)
    set_servo_pulse_all(pwm,700)
    #print("okay, you have 5, connect battery")
    # time.sleep(5)
    #raw_input("ready to go?")
    # calibrate(pwm,1000,2000)
    # sys.exit(0)
    #print("let's try")
    #1035 is lowest it responds
    rospy.init_node('pwm_motor_controller', anonymous=True)
    sub = rospy.Subscriber('motor_control', Float32MultiArray, cb)
    rate = rospy.Rate(60)
    while not rospy.is_shutdown():
        data_age=time.time()-data_received_time
        if data_age>.5:
            #rospy.loginfo("No recent data, setting all motors to 700")
            set_servo_pulse_all(pwm,700)
            continue;
        try:
            for (channel,val) in enumerate(data):
                #rospy.loginfo("setting motor "+str(channel)+" to "+str(1035+val*SCALAR))
                set_servo_pulse(pwm,channel,1035+val*SCALAR)
        except:
            pass
    set_servo_pulse_all(pwm,700)
if __name__ == "__main__":
    main()
