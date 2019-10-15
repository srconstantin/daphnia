#!/usr/bin/python3.6
from datetime import datetime
from pypylon import pylon
import platform
import imageio
import time
from math import floor
import os
import convertimages
import awsexport

#Most recent pylon video capture script. Captures a specified number of frames at a specified framerate (both hardcoded).
#Stores a video of the capture (currently in /dev/shm), as well as a folder containing all the frames captured (saved as PNGs), with the folder named after the current time UTC, in ISO format.

#The boolean value debug, when set to true, will log this script's activity in the file capture.log, and print various messages about the script's progress.


debug = True;

#writes a message to the file capture.log, with a UTC timestamp
def writeToLog(message):
    f = open('capture.log', mode='a')
    print(str(datetime.utcnow()) + '  -    ' + message, file=f)

#writes a message to the file capture.log as well as to stdout, with a UTC timestam on
def writeEverywhere(message):
    f = open('capture.log', mode='a')
    print(str(datetime.utcnow()) + '  -    ' + message, file=f)
    print(str(datetime.utcnow()) + '  -    ' + message)

#fetch camera connected to computer
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
#parameters for video capture. Batch size is how many images are captured at a time before writing the images from memory to disk.
batch_size = 100
video_fps = 30.0
exposure = floor(1000000 / video_fps)
config_string = "# {05D8C294-F295-4dfb-9D01-096BD04049F4}\nExposureAuto\tOff\nGainAuto\tOff\nWidth\t2048\nHeight\t2048\nExposureMode\tTimed\nExposureTime\t%.01f\n" % (exposure)

if debug:
    writeEverywhere('Starting capture: ' + str(video_fps) + ' fps')
if debug:
    writeEverywhere('Config string: ' + str(config_string))

conv = pylon.ImageFormatConverter()

conv.OutputPixelFormat = pylon.PixelType_BGR8packed
conv.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

#create UTC date and time string, omitting everything after the decimal point as it will be used in a filename.
rightnow = datetime.utcnow().isoformat()

cleannow = ''

for char in rightnow:
    if char in '0123456789T':
        cleannow += str(char)
    elif char == '.':
        break
#make a folder to put the video output, and initialize the output file.
os.mkdir(cleannow)
#change '/home/alyssa/pypylon to the directory where the folders containing mkvs and images are to be stored.
outputfile = '/home/alyssa/pypylon/' + cleannow +'/' + cleannow + '.mkv'

print(outputfile)

writer = imageio.get_writer(outputfile, fps=video_fps, output_params=['-crf', '18'])

camera.OutputQueueSize = 15

#start recording video
camera.StartGrabbing(pylon.GrabStrategy_LatestImages)

#parameters for video recording. TotalFrames is the frame number over all batches, while frames is the frame number in the current batch.
totalFrames = 0
images = []
grabResults = []
frames = 0
while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        image = conv.Convert(grabResult)
        images.append(image)
        frames = frames + 1
        totalFrames += 1
        print(totalFrames)
        #change the line below for different amounts of frames in the video.
        if totalFrames > 1000:
            images = []
            break
        #every batch, write the captured images to the mkv file, and clear the array of images ftom memory.
        elif frames >= batch_size:
            frames = 0
            while images != []:
                image = images.pop(0)
                frames += 1
                img = image.GetArray()
                writer.append_data(img)
            frames = 0

    grabResult.Release()

frames = 0
if debug:
    writeEverywhere("Attempting to create directory.")



camera.StopGrabbing()
writer.close()

#see convertimages.py; this converts the video in the newly created directory to its component images as JPGs, and places those JPGs into the same directory.
convertimages.convert_all(cleannow)

#see awsexport.py; this uploads every file in the newly created directory to an AWS S3 bucket, called daphniavideo.
awsexport.upload_all(cleannow)

if debug:
    writeEverywhere("captured video")
