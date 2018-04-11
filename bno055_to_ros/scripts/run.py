#!/usr/bin/env python
import os
import sys
import time
from Adafruit_BNO055 import BNO055
# rosmsg list, rosmsg show
#sensor_msgs/Temperature
#sensor_msgs/Imu
import sensor_msgs.msg as sensor_msgs
import std_msgs.msg as std_msgs
import rospy

def main():
    imupub = rospy.Publisher("imu",sensor_msgs.Imu, queue_size=10)
    rospy.init_node("imu",anonymous=False)
    bno = BNO055.BNO055()
    if not bno.begin():
        raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')
    status, self_test, error = bno.get_system_status()
    print('System status: {0}'.format(status))
    print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
    sw, bl, accel, mag, gyro = bno.get_revision()
    print('Software version:   {0}'.format(sw))
    print('Bootloader version: {0}'.format(bl))
    print('Accelerometer ID:   0x{0:02X}'.format(accel))
    print('Magnetometer ID:    0x{0:02X}'.format(mag))
    print('Gyroscope ID:       0x{0:02X}\n'.format(gyro))
    rate = rospy.Rate(60)
    while not rospy.is_shutdown():
        imumsg = sensor_msgs.Imu()
        sys, gyro, accel, mag = bno.get_calibration_status()
        qx,qy,qz,qw = bno.read_quaternion()
        imumsg.orientation.x = qx
        imumsg.orientation.y = qy
        imumsg.orientation.z = qz
        imumsg.orientation.w = qw
        lax,lay,laz = bno.read_linear_acceleration()
        imumsg.linear_acceleration.x = lax
        imumsg.linear_acceleration.y = lay
        imumsg.linear_acceleration.z = laz
        #rospy.loginfo(imumsg)
        imupub.publish(imumsg)
        rate.sleep()




if __name__ == "__main__":
    main()
