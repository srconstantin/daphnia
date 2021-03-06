#!/usr/bin/python3.6


#this video capture script is outdated. Use pylonvideo-06042019.py instead.
from datetime import datetime
from pypylon import pylon
import platform
import imageio
import time
from math import floor

camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

video_fps = 30.0
exposure = floor(1000000 / video_fps)
config_string = "# {05D8C294-F295-4dfb-9D01-096BD04049F4}\nExposureAuto\tOff\nGainAuto\tOff\nWidth\t2048\nHeight\t2048\nExposureMode\tTimed\nExposureTime\t%.01f\n" % (exposure)


conv = pylon.ImageFormatConverter()

conv.OutputPixelFormat = pylon.PixelType_BGR8packed
conv.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

rightnow = datetime.utcnow().isoformat()

cleannow = ''

for char in rightnow:
   if char in '0123456789T':
        cleannow += str(char)
   elif char == '.':
        break

outputfile = '/dev/shm/pylon-capture-' + cleannow +'.mkv'

print(outputfile)

writer = imageio.get_writer(outputfile, fps=video_fps, output_params=['-crf', '18'])

camera.OutputQueueSize = 15
camera.StartGrabbing(pylon.GrabStrategy_LatestImages)

frames = 0
images = []
while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        image = conv.Convert(grabResult)
        images.append(image)
        frames = frames + 1
        print(frames)
        if frames >= 150:
            break

    grabResult.Release()

for image in images:
    img = image.GetArray()
    writer.append_data(img)

camera.StopGrabbing()
writer.close()
