#!/usr/bin/python3.6

#Correct script for reformatting train.txt and test.txt for py-faster-rcnn. 
#Removes extensions from filenames in train.txt and test.txt, so py-faster-rcnn can interpret them.

train_old = open("train.txt", "r")

test_old = open("test.txt", "r")

train_new = open("train_faster.txt", "w")

test_new = open("test_faster.txt", "w")

row = train_old.readline()
while(len(row) > 2):
       floyd_path = row.split("/")
       jpg_filename = floyd_path[len(floyd_path) - 1]
       filename = jpg_filename[:len(jpg_filename) - 5]
       train_new.write(filename + "\n")
       row = train_old.readline()

row = test_old.readline()
while(len(row) > 2):
       floyd_path = row.split("/")
       jpg_filename = floyd_path[len(floyd_path) - 1]
       filename = jpg_filename[:len(jpg_filename) - 5]
       test_new.write(filename + "\n")
       row = test_old.readline()
