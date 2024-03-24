"""
MIT BWSI Cubesat Challenge
MIT license

File Name: CubesatCamera.py

Title: Cubesat Camera

Author: Jeremy Wang (MASSBUILDERS)

Purpose: This code will interface all of the electrical components of the Cubesat and will first take a picture using a camera, then send the image to github
"""

#Imports
import numpy
import time

import board
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL
from picamera2  import Picamera2

#Git Setup
from git import Repo

repo = Repo("/home/massbuilders/sat")
image_path = "/home/massbuilders/sat/images"

#IMU Setup
i2c = board.I2C()
gyro = LSM6DS(i2c) #gyro+accel
mag = LIS3MDL(i2c) #magnetometer

#test code
while(True):
    print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (gyro.acceleration))
    print("Gyro X:%.2f, Y: %.2f, Z: %.2f degrees/s" % (gyro.gyro))
    print("")
    time.sleep(0.5)