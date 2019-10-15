#!/usr/bin/python3.6


#This script generates a CSV with labels from Darknet-formatted train.txt, test.txt, and label txt files. Labels in the CSV are formatted (xmin, ymin, xmax, ymax) on an absolute pixel scale.

import pandas

def generate_csv(filelist_path, dataset_path):
    labellist = []
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    filelist = open(filelist_path, "r")
    #iterate over each image and set of labels
    row = filelist.readline()
    while(len(row) > 2):
        floyd_path = row.split("/")
        jpg_filename = floyd_path[len(floyd_path) - 1]
        filename = jpg_filename[:len(jpg_filename) - 4] + "txt"
        #read label file, iterate over each label.
        labels = open(dataset_path + "/" + filename, "r")
        label = labels.readline().split(" ")
        while len(label) > 2:
            #scale up to absolute pixel values
            x_ctr = float(label[1]) * 2048
            y_ctr = float(label[2]) * 2048
            box_width = float(label[3]) * 2048
            box_height = float(label[4]) * 2048
            #remove newline character at the end of jpg filename
            entry = (jpg_filename[:(len(jpg_filename) - 1)], 2048, 2048, "daphnia", (x_ctr - box_width/2.0) + 1, (y_ctr - box_height/2.0) + 1, x_ctr + box_width/2.0, y_ctr + box_height/2.0)
            labellist.append(entry)
            label = labels.readline().split(" ")
        row = filelist.readline()
    frame = pandas.DataFrame(labellist, columns=column_name)
    return frame

#Edit output CSV, file list, image and label directory here.
frame = generate_csv("/home/alyssa/test.txt", "/home/alyssa/datasets/20190708t212659")
frame.to_csv("test_labels.csv", index=None)


