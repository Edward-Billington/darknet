# Iterate through each model.

import os
path_to_darknet = "/home/edward/Documents/darknet/"
images_count = 17

files = {
	"yolov3-voc-v5_final.weights": "yolov3-voc-v5.cfg"
}

for file in files:
	weight_file = path_to_darknet + "backup/" + file
	config_file = path_to_darknet + "cfg/" + files[file]

	# GO THROUGH EACH MODEL
	for i in range(1, images_count+1):
		# number 7 is png
		filetype = ".jpg" if i != 7 else ".png"
		filepath = path_to_darknet + "data/testing_images/knife_image_" + str(i) + filetype
		cmd = "./darknet detector test cfg/voc.data " + config_file + " " + weight_file + " " + filepath
		out = path_to_darknet + "results/" + files[file]+"_image_" + str(i) +".txt"
		os.system(cmd + " > " + out)
