import os

command = "./darknet detector test cfg/voc.data cfg/yolov3-voc.cfg backup/yolov3-voc_final.weights data/knife_image_3.jpg"
os.system(command)
