#!/usr/bin/python3.6
import os
from PIL import Image
import cv2
#This script converts every video in a directory into several JPG images per video, one per frame.
#Because Pylon capture cannot output JPGs directly, this script is called to convert the captured MKV video file to JPGs.


def convert_all(directory):
    #fetch file names in directory (assumed only videos)
    videos = os.listdir(directory)
    for video in videos:
        #use cv2 video capture to read the video frame by frame
        capture = cv2.VideoCapture(directory + '/' + video)
        success, img = capture.read()
        frames = 1
        while success:
            #write each frame to a file specifying the frame number while there are still frames to read.
            cv2.imwrite(directory + '/' + directory + '-frame-' + zero_pad(frames) + '.jpg', img)
            success, img = capture.read()
            frames += 1

#turns a frame number into the corresponding zero-padded string, so that frame 100 is listed after frame 11, etc. 
def zero_pad(num):
    if num < 10:
        return "000" + str(num)
    elif num < 100:
        return "00" + str(num)
    elif num < 1000:
        return "0" + str(num)
    else:
        return str(num)

print(zero_pad(6))

print(zero_pad(66))

print(zero_pad(666))

print(zero_pad(6666))
