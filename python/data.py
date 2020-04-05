# Iterate through each model.

import os
path_to_darknet = "/home/edward/Documents/darknet/"

files = {
	"yolov3-voc_final.weights": "yolov3-voc.cfg",
	"yolov3-voc-v2_final.weights": "yolov3-voc-v2.cfg",
	"yolov3-voc-v3_final.weights": "yolov3-voc-v3.cfg",
	"yolov3-voc-v4_final.weights": "yolov3-voc-v4.cfg",
}

images = [
	"knife_image_1.jpg"
]

for file in files:
	weight_file = path_to_darknet + "backup/" + file
	config_file = path_to_darknet + "cfg/" + files[file]
	os.system("cat "+config_file)
	for a in images:
		print(a)
	break