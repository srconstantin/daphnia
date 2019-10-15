#!/usr/bin/python3.6

#reformats Labelbox label CSV to multiple txt files, formatted for Darknet: x-center, y-center, width, and height, all relative to image size. Labels in the Labelbox CSV are formatted as a JSON or similar, with an entry for each of the four corners of a box.

img_height = 2048.0

img_width = 2048.0


def make_label_file(row, path):
    #replace comma containing separators for easier parsing by splitting at commas
    row = row.replace("},{", "};{")
    row = row.replace(",\"\"y", ";\"\"y")
    #Add three placeholder characters to box separator, to avoid truncation of final y-value.
    #TODO: Possibly replace these parsing mechanisms with regexes.
    row = row.replace("}]}", "...}]}")
    print(row)
    entries = row.split(',')
    filename = entries[9]
    filename = filename[:len(filename) - 4] + ".txt"
    f = open(path + "/" + filename, "w")
    boxes = entries[3].split("}]}")
    for box in boxes:
        lowest_x = 999999999
        highest_x = 0
        lowest_y = 999999999
        highest_y = 0
        points = box.split("\"\"")
        #find highest and lowest x and y values per box, use them to compute center coordinates, width, and jheight.
        for i in range(len(points)):
            if "x" in points[i]:
                xval = points[i+1]
                xval = xval[1:(len(xval) - 1)]
                lowest_x = min(lowest_x, int(xval))
                highest_x = max(highest_x, int(xval))
            elif "y" in points[i]:
                yval = points[i+1]
                yval = yval[1:(len(yval) - 3)]
                if len(yval) > 0:
                    lowest_y = min(lowest_y, int(yval))
                    highest_y = max(highest_y, int(yval))
        width = (highest_x - lowest_x)/img_width
        height = (highest_y - lowest_y)/img_height
        print(highest_x)
        print(lowest_x)
        x_center =  (((highest_x + lowest_x)/2.0) - 1.0)/img_width
        y_center = (((highest_y + lowest_y)/2.0) - 1.0)/img_height
        if x_center < 1:
            print("0 " + str(x_center) + " " + str(y_center) + " " + str(width) + " " + str(height))
            print("0 " + str(x_center) + " " + str(y_center) + " " + str(width) + " " + str(height), file=f)

#edit to specify csv and output path.
csv = open("/home/alyssa/Documents/export-2019-08-16T23_36_27.654Z.csv", "r")
row = csv.readline()
row = csv.readline()
while(len(row) > 2):
    make_label_file(row, "/home/alyssa/labels")
    row = csv.readline()
                
    
