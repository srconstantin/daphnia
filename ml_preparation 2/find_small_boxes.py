#!/usr/bin/python

#finds any boxes that are 33 pixels or less on a side. Outdated, as that was not the problem causing the bug this file was intended to fix.

def find_small_boxes(filelist_path, dataset_path):
    filelist = open(filelist_path, "r")
    row = filelist.readline()
    while(len(row) > 2):
        floyd_path = row.split("/")
        jpg_filename = floyd_path[len(floyd_path) - 1]
        filename = jpg_filename[:len(jpg_filename) - 4] + "txt"
        labels = open(dataset_path + "/" + filename, "r")
        label = labels.readline().split(" ")
        while len(label) > 2:
            box_width = float(label[3]) * 2048
            box_height = float(label[4]) * 2048
            if box_width < 33 or box_height < 33:
                print(filename)
            label = labels.readline().split(" ")
        row = filelist.readline()

find_small_boxes("/home/alyssa/train.txt", "/home/alyssa/datasets/20190708t212659")
