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

repo = Repo("/home/pi/sat")
image_path = "/home/pi/sat/images"
