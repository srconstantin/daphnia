#!/bin/bash

# Camera input capture script (hoopty)
# JPxGotts / 2019 March 20 / GPL V3.0
# -----------------------------------
# Simple command-line script that captures JPEGs from a video device.
# Some parts of this script must be edited to use it properly.
#
# To run this script, you must have either "streamer" or "scrot" installed.
#   streamer is the package for capturing directly from video devices.
#   scrot is the package for capturing screenshots directly.
#   To install them, use apt-get, yum or a package manager of your choice.
# 
# "/dev/video0" should be replaced with whatever your device is mounted to.
#    To list all mounted video devices, use the following command:
#    ls -al /sys/class/video4linux
#    To get a listing of video devices with names, I used VLC's GUI.
#   
# "DIRECTORY" should be replaced with the path that you want the files in.
#    Do not put a trailing slash on the end of it. This kills the script.
#    For example: "/home/jpxg/srsbiz/lab/data/screenshots".
#
# The default behavior is a 30-second interval. This can be adjusted.
#    All of the numbers after the "sleep" lines, put together, make 30.
#    If you change them, you can make the interval longer or shorter.
#    You can remove the "echo" lines and the program will still work.

cd DIRECTORY
while true
do 	

now=$(date +"%Y-%m-%dT%H:%M:%S")

# DISPLAY=:0 scrot 'DIRECTORY/data-%Y-%m-%d-%H_%M_%S.jpg' -q 20
#   Use this line, and comment out the other one, if you want the entire screen instead of the video device.

streamer -c /dev/video0 -b 16 -o "DIRECTORY/data-$now.jpeg"
echo "Screenshot saved. Next one in 30 seconds."
sleep 5
echo "25"
sleep 5
echo "20"
sleep 5
echo "15"
sleep 5
echo "10"
sleep 5
echo "5"
sleep 1
echo "4"
sleep 1
echo "3"
sleep 1
echo "2"
sleep 1
echo "1"
sleep 1
done
