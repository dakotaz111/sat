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
from datetime import datetime

import board
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL
from picamera2  import Picamera2, Preview

#Git Setup
from git import Repo

repo = Repo("/home/massbuilders/sat")

#IMU Setup
i2c = board.I2C()
gyro = LSM6DS(i2c) #gyro+accel
mag = LIS3MDL(i2c) #magnetometer

#Camera Setup
picam2=Picamera2()
config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores") # adjust img size here
picam2.configure(config)

def git_push():
    origin = repo.remote('origin')
    print('added remote')
    origin.pull()
    print('pulled changes')
    repo.git.add("/home/massbuilders/sat/images")
    repo.index.commit('New Photo')
    print('made the commit')
    origin.push()
    print('pushed changes')
    picam2.stop()

def name():
    now = datetime.now()
    date = now.strftime("%m-%d-%Y_%H-%M-%S")
    name = f"/home/massbuilders/sat/images/{date}.jpg"
    return name

#test code

#code to take pic
picam2.start()
time.sleep(2)
picam2.capture_file(name())
picam2.stop()
git_push()

# while(True):
#     # print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (gyro.acceleration))
#     print("Gyro X:%.2f, Y: %.2f, Z: %.2f degrees/s" % (gyro.gyro))