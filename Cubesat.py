import cv2
import numpy as np

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
    processedImg = cv2.inRange(image, (200,200,200), (255,255,255)) # lower/upper thresholds for white
    pixels = processedImg.tolist()
    black_coords = []
    white_coords = []

    # Pixel iteration
    for x in range(len(pixels)):
        for y in range(len(pixels[x])):
            if pixels[x][y] == 0:
                black_coords.append((x, y))
                color_amount["black"] += 1
            elif pixels[x][y] == 255:
                white_coords.append((x, y))
                color_amount["white"] += 1
    
    total_pixels = image.shape[0] * image.shape[1]
    perc_red = color_amount["red"] / total_pixels
    perc_green = color_amount["green"] / total_pixels
    perc_blue = color_amount["blue"] / total_pixels
    
    return (processedImg, black_coords, white_coords, perc_red, perc_green, perc_blue);
   
#Main code that is being run
def color_id(image_file = 'test.jpg'):
    folder_path = '/home/pi/sat' #Replace with the folder path for the folder in the
                     #Flat Sat Challenge with your name so you can view images
                     #on Github if you don't have VNC/X forwarding

    image = cv2.imread('images/' + image_file) #Converts image to numpy array in BGR format
    
    processedImg, black_coords, white_coords, perc_blue, perc_green, perc_red = processing(image)
    
    cv2.imwrite(folder_path + 'processedImg.jpg', processedImg)


""" This code is for command line entry. It allows you to add arguments 
    for what you want the code to run on. For instance, if I want to run 
    it on an image called "test1.jpg" with visualizations on, I would 
    type python3 color_id.py test1.jpg True
"""
if __name__ == '__main__':
    import sys
    
    color_id(*sys.argv[1:])
