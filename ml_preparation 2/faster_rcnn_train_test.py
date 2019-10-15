#!/usr/bin/python3.6

#outdated, this separates all the images, rather than only the labeled ones. Usable when all the frames of 0708t212659 have been labeled.

i = 1

file_train = open("train_faster_rcnn.txt", "w")

file_test = open("test_faster_rcnn.txt", "w")

while i <= 5900:
    if i % 10 != 0:
        file_train.write("20190708T212659-frame-" + str(i) +"\n")
    else:
        file_test.write("20190708T212659-frame-" + str(i) + "\n")
    i += 1
