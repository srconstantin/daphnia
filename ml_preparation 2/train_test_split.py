#!/usr/bin/python3.6

import glob
import os
#import Tkinter
#import Tkconstants
#import tkFileDialog


#Splits labeled images into train.txt and test.txt for Darknet Yolo.

labeled_images = os.listdir("/home/alyssa/labels")

valid_titles = []

for img in labeled_images:
    valid_titles.append(img[:len(img) - 4])


current_dir = "/home/alyssa/pypylon/20190708T212659"

#while True:
    #print("Please select your image directory.")
   # current_dir = tkFileDialog.askdirectory()
   # if current_dir == None or current_dir == "":
     #   print("You must select a directory.")
     #   continue
   # break
# Percentage of images to be used for the test set
percentage_test = 10
# Create and/or truncate train.txt and test.txt
file_train = open('train.txt', 'w')
file_test = open('test.txt', 'w')
# Populate train.txt and test.txt
counter = 1
index_test = round(100 / percentage_test)
for pathAndFilename in glob.iglob(os.path.join(current_dir, "*.jpg")):
    title, ext = os.path.splitext(os.path.basename(pathAndFilename))
    if counter == index_test and title in valid_titles:
        counter = 1
        #You can change the path in the list to refer to other locations depending on where you are running Darknet.
        file_test.write("/floyd/input/20190708t212659" + "/" + title + '.jpg' + "\n")
    elif title in valid_titles:
        file_train.write("/floyd/input/20190708t212659" + "/" + title + '.jpg' + "\n")
        counter = counter + 1


