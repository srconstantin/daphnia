# run.sh - JPG 2019-06-05
# bash script, run from crontab, that calls the pylon video capture script. Change the directory to wherever the capture script is stored.
cd /home/alyssa/pypylon
echo "Attempting to run script." >> run.log
python3 pylonvideo-06042019.py
# TODO: put iso timestamp in the line that writes to run.log 
