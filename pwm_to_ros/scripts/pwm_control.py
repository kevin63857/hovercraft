#!/usr/bin/env python

import sys
import time
import rospy
import Adafruit_PCA9685

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

def main():
    low = 1000
    high = 2000
    pwm = Adafruit_PCA9685.PCA9685()
    pwm.set_pwm_freq(60)
    set_servo_pulse_all(pwm,700)
    print("okay, you have 5, connect battery")
    # time.sleep(5)
    raw_input("ready to go?")
    # calibrate(pwm,1000,2000)
    # sys.exit(0)
    print("let's try")
    #1035 is lowest it responds
    try:
        for i in range(100):
            set_servo_pulse_all(pwm,1030+i)
            time.sleep(.001)
            raw_input(".")
            print("i=%d"%i)

    except:
        pass
    set_servo_pulse_all(pwm,700)




if __name__ == "__main__":
    main()
