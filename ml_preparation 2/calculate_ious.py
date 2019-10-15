#!/usr/bin/python3.6

# Finds the average maximum IOU above a given threshold in a Darknet validation set detection file.
# Specifically, reads in the detection file, and for each box detected above the threshold:
#  Finds the IOU with each box labeled in the image, after converting the label format to absolute pixel values.
#  Takes the maximum of all IOUs seen for the box, and adds it to a running total, later divided by the number of boxes detected.

#edit probability threshold here

probability_threshold = .0505
image_height = 2048.0
image_width = 2048.0

def calculate_precision(detection_path, label_directory):
    detection = open(detection_path, "r")
    row = detection.readline()
    num_boxes = 0
    iou_total = 0.0
    while len(row) > 2:
        box = row.split(" ")
        if float(box[1]) > probability_threshold:
            corners = [float(box[2]), float(box[3]), float(box[4]), float(box[5])]
            num_boxes += 1
            frame_path = label_directory + "/" + box[0] + ".txt"
            frame_labels = open(frame_path, "r")
            label = frame_labels.readline().split(" ")
            best_iou = 0.0
            while len(label) > 2:
                true_corners = convert_to_absolute(float(label[1]), float(label[2]), float(label[3]), float(label[4])) 
                union = (true_corners[3] - true_corners[1]) * (true_corners[2] - true_corners[0]) + (corners[3] - corners[1]) * (corners[2] - corners[0])
                xs = [corners[0], corners[2], true_corners[0], true_corners[2]]
                xs.sort()
                ys = [corners[1], corners[3], true_corners[1], true_corners[3]]
                ys.sort()
                if intersect(xs, ys, corners, true_corners):
                    intersection = abs( (xs[2] - xs[1]) * (ys[2] - ys[1]))
                else:
                    intersection = 0.0
                iou = intersection/union
                if iou > best_iou:
                    best_iou = iou
                label = frame_labels.readline().split(" ")
            iou_total += best_iou
            print(best_iou)
        row = detection.readline()
    print(iou_total/num_boxes) 




def convert_to_absolute(x_center, y_center, width, height):
     return [(x_center - width/2.0) * image_width, (y_center - height/2.0) * image_height, (x_center + width/2.0) * image_width, (y_center + height/2.0) * image_height]


def intersect(xs, ys, corners, true_corners):
    if (xs[0] in corners and xs[2] in corners) or (xs[0] in true_corners and xs[2] in true_corners):
        return (ys[0] in corners and ys[2] in corners) or (ys[0] in true_corners and ys[2] in true_corners)
    else:
        return False
#edit detection file to read and label files to compare to here.
calculate_precision("/home/alyssa/Downloads/comp4_det_test_daphnia.txt", "/home/alyssa/pypylon/20190708T212659")

 
