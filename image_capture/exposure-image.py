#!/usr/bin/python3.6
from pypylon import pylon
import sys
import platform

#this is a sample script, that captures a single image with a provided exposure time in the system arguments, and saves it to disk in this file's directory.

if len(sys.argv) < 2:
    sys.exit("Must provide exposure time in float as first argument!")

new_exposure = sys.argv[1]

img = pylon.PylonImage()
tlf = pylon.TlFactory.GetInstance()

camera = pylon.InstantCamera(tlf.CreateFirstDevice())
camera.Open()

cur_config = pylon.FeaturePersistence.SaveToString(camera.GetNodeMap())
exposure_idx = cur_config.find("ExposureTime")
print(exposure_idx)
exposure_val = cur_config[exposure_idx+13:exposure_idx+25].partition('\n')[0]
print(exposure_val)
cur_config = cur_config.replace(exposure_val, new_exposure)
pylon.FeaturePersistence.LoadFromString(cur_config, camera.GetNodeMap(), True)

camera.StartGrabbing()
with camera.RetrieveResult(2000) as result:
    img.AttachGrabResultBuffer(result)
    img.Save(pylon.ImageFileFormat_Png, "expimage.png")
    img.Release()

camera.StopGrabbing()
camera.Close()
