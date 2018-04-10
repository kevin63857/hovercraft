#!/bin/python
#Python
import smbus
import math
import time

PCA9685_SUBADR1=0x2
PCA9685_SUBADR2=0x3
PCA9685_SUBADR3=0x4

PCA9685_MODE1=0x0
PCA9685_PRESCALE=0xFE

LED0_ON_L=0x6
LED0_ON_H=0x7
LED0_OFF_L=0x8
LED0_OFF_H=0x9

ALLLED_ON_L=0xFA
ALLLED_ON_H=0xFB
ALLLED_OFF_L=0xFC
ALLLED_OFF_H=0xFD

#Class that stores state and functions for interacting with PCA9685 PWM chip
class Adafruit_PWMServoDriver:
    def __init__(self, addr = 0x40):
        self.i2c_addr = addr
        self.bus=smbus.SMBus(1)

    def begin(self):
        #self.bus.begin()
        #self.reset()
        self.setPWMFreq(1000)

    def reset(self):
        self.write8(0x80, PCA9685_MODE1)
        self.delay(10)

    def setPWMFreq(self, freq):
        freq *= 0.9  # Correct for overshoot in the frequency setting (see issue #11).
        pre_scale_val = 25000000
        pre_scale_val/=4096
        pre_scale_val/=freq
        pre_scale_val-=1
        prescale = int(math.floor(pre_scale_val + 0.5))
        oldmode = self.read8(PCA9685_MODE1);
        newmode = (oldmode&0x7F) | 0x10; #sleep
        self.write8(newmode,PCA9685_MODE1); #go to sleep
        self.write8(prescale,PCA9685_PRESCALE); #set the prescaler
        self.write8(oldmode,PCA9685_MODE1);
        #time.sleep(5);
        self.write8(oldmode | 0xa0,PCA9685_MODE1);  #This sets the MODE1 register to turn on auto increment.


    def setPWM(self, num, on, off):
        self.write8(LED0_ON_L+4*num);
        self.write8(on);
        self.write8(on>>8);
        self.write8(off);
        self.write8(off>>8);

    def setPin(self, num, val, invert=False):
        # Clamp value between 0 and 4095 inclusive.
        val = math.min(val, 4095)
        if invert:
            if val == 0:
                # Special value for signal fully on.
                setPWM(num, 4096, 0)
            elif val == 4095:
                # Special value for signal fully off.
                setPWM(num, 0, 4096)
            else:
                setPWM(num, 0, 4095-val)
        else:
            if val == 4095:
                #  Special value for signal fully on.
                setPWM(num, 4096, 0)
            elif val == 0:
                # Special value for signal fully off.
                setPWM(num, 0, 4096)
            else:
                setPWM(num, 0, val)

    def read8(self, addr=None):
        if addr is None:
            addr=self.i2c_addr
        return self.bus.read_byte(addr)

    def write8(self, d, addr=None):
        print addr,d
        if addr is not None:
            self.bus.write_byte(self.i2c_addr,addr)
        self.bus.write_byte(self.i2c_addr,d)


if __name__ == '__main__':
    pwm = Adafruit_PWMServoDriver()
    # you can also call it with a different address you want
    #Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x41);
    # you can also call it with a different address and I2C interface
    #Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(&Wire, 0x40);
    print "16 channel PWM test!"
    pwm.begin();
    pwm.setPWMFreq(1600);  # This is the maximum PWM frequency

    while True:
        # Drive each PWM in a 'wave'
        for i in xrange(0,4096,8):
            for pwmnum in range(0,16):
                pwm.setPWM(pwmnum, 0, (i + (4096/16)*pwmnum) % 4096 )
