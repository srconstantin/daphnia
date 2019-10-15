#!/usr/bin/python3.6

#copies images and labels specified by train.txt or test.txt from one directory to another, used here to separate the training set from the test set. 

import os
import shutil

def copy_all_specified(from_dir, to_dir, filelist_path):
    filelist = open(filelist_path, "r")
    row = filelist.readline()
    while(len(row) > 2):
        floydpath = row.split("/")
        jpg_filename = floydpath[len(floydpath) - 1]
        if jpg_filename[len(jpg_filename) -1] != 'g':
            jpg_filename = jpg_filename[:len(jpg_filename) - 1]
        txt_filename = jpg_filename[:len(jpg_filename) - 3] + "txt"
        print(txt_filename)
        shutil.copy(from_dir + "/" + jpg_filename, to_dir)
        shutil.copy(from_dir + "/" + txt_filename, to_dir)
        row = filelist.readline()

#edit directories and file list that specifies what is to be copied here.
copy_all_specified("/home/alyssa/datasets/20190708t212659", "/home/alyssa/datasets/20190708t212659-tensorflow/test", "/home/alyssa/test.txt")
