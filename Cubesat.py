"""
MIT BWSI Cubesat Challenge
MIT license

File Name: CubesatCamera.py

Title: Cubesat Camera

Author: Jeremy Wang (MASSBUILDERS)

Purpose: This code will interface all of the electrical components of the Cubesat and will first take a picture using a camera, then send the image to github
"""

#Imports
import time
from datetime import datetime
import cv2
import numpy as np
import csv


import board
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL
from picamera2  import Picamera2, Preview

#Git Setup
from git import Repo
outageSectors = []
outageSectors.append(1)
outageSectors.append(3)
outageSectors.append(7)


repo = Repo("/home/massbuilders/sat")

black_coords = []
white_coords = []
perc_black = 0
#IMU Setup
i2c = board.I2C()
gyro = LSM6DS(i2c) #gyro+accel
mag = LIS3MDL(i2c) #magnetometer

#Camera Setup
picam2=Picamera2()
config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores") # adjust img size here
picam2.configure(config)

def git_push():
    file.close()
    origin = repo.remote('origin')
    print('added remote')
    origin.pull()
    print('pulled changes')
    repo.git.add("/home/massbuilders/sat/Cubesat.py")
    repo.git.add("/home/massbuilders/sat/images")
    repo.git.add("/home/massbuilders/sat/processedData.csv")
    repo.index.commit('New Photo')
    print('made the commit')
    origin.push()
    print('pushed changes')
    picam2.stop()

def naming():
    now = datetime.now()
    date = now.strftime("%m-%d-%Y_%H-%M-%S")
    name = f"/home/massbuilders/sat/images/{date}.jpg"
    return name

name = naming()

#Script for determining the percentage of each color using PIL and using
#RGB representation. When running in the command line, type the image file.

def get_mask(image, lower_bound, upper_bound):
    threshold = cv2.inRange(image, lower_bound, upper_bound)
    mask = cv2.bitwise_and(image, image, mask=threshold)
    return cv2.bitwise_and(image, mask)

def processing(image):
    #Counter for amount of pixels of each color
    color_amount = {"black":0, "white":0}
        
    #PART 1: COLOR IDENTIFICATION
    processedImg = cv2.inRange(image, (0,0,0), (75,75,75)) # lower/upper thresholds for white
    pixels = processedImg.tolist()

    # Pixel iteration
    for x in range(len(pixels)):
        for y in range(len(pixels[x])):
            if pixels[x][y] == 255:
                black_coords.append((x, y))
                color_amount["black"] += 1
            elif pixels[x][y] == 0:
                white_coords.append((x, y))
                color_amount["white"] += 1
    
    total_pixels = image.shape[0] * image.shape[1]
    global perc_black
    perc_black = color_amount["black"] / total_pixels
    global perc_white
    perc_white = color_amount["white"] / total_pixels
    
    return (processedImg, black_coords, white_coords, perc_black, perc_white);
   
#Main code that is being run
def color_id(image_file):
    folder_path = f'/home/massbuilders/sat/' #Replace with the folder path for the folder in the
                     #Flat Sat Challenge with your name so you can view images
                     #on Github if you don't have VNC/X forwarding

    image = cv2.imread(name) #Converts image to numpy array in BGR format
    
    processedImg, black_coords, white_coords, perc_black, perc_white = processing(image)
    print(perc_black)
    cv2.imwrite(folder_path + 'images/processedImg.jpg', processedImg)

#test code


picam2.start()
time.sleep(2)
name = naming()
picam2.capture_file(name)
picam2.stop()

# while(True):
#     # print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (gyro.acceleration))
#     print("Gyro X:%.2f, Y: %.2f, Z: %.2f degrees/s" % (gyro.gyro))

""" This code is for command line entry. It allows you to add arguments 
    for what you want the code to run on. For instance, if I want to run 
    it on an image called "test1.jpg" with visualizations on, I would 
    type python3 color_id.py test1.jpg True
"""
if __name__ == '__main__':
    import sys
    
    color_id(*sys.argv[1:])
    data = outageSectors
    with open('/home/massbuilders/sat/processedData.csv','w') as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(["Date",name[30:-4]])
        csvwriter.writerow(data)
        csvwriter.writerow(["Percent of city without power",perc_black*100])
    git_push()
