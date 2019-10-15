#!/usr/bin/python3.6
from pypylon import pylon
import platform
import sys, os

# Ryan K, 5/2019
# Relatively simple pypylon script to just take one simple image from the camera.
# Specify the gain and exposure time.
if len(sys.argv) < 4:
    sys.exit("Usage: %s <exposure> <gain> <output file>" % (sys.argv[0]))

exposure_val = round(float(sys.argv[1]), 0)
gain_val = float(sys.argv[2])

# string for configuration to set exposure and gain, w/ magic number
config_string = "# {05D8C294-F295-4dfb-9D01-096BD04049F4}\nExposureAuto\tOff\nGainAuto\tOff\nWidth\t2048\nHeight\t2048\nExposureMode\tTimed\nExposureTime\t%.01f\nGainSelector\tAll\nGain\t%.05f\n" % (exposure_val, gain_val)
output_file = sys.argv[3]
if not os.path.isdir(os.path.dirname(os.path.abspath(output_file))):
    sys.exit("Error: cannot write to file %s" % output_file)
img = pylon.PylonImage()
tlf = pylon.TlFactory.GetInstance()

camera = pylon.InstantCamera(tlf.CreateFirstDevice())
camera.Open()
pylon.FeaturePersistence.LoadFromString(config_string, camera.GetNodeMap(), True)

camera.StartGrabbing()
with camera.RetrieveResult(2000) as result:
    img.AttachGrabResultBuffer(result)
    img.Save(pylon.ImageFileFormat_Png, output_file)
    img.Release()
camera.StopGrabbing()
camera.Close()
