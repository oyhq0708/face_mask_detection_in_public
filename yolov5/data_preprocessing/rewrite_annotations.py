#!/usr/bin/env python3

import json
import os

def readAnnotations(filename):
    # Opening JSON file
    f = open(filename)
	
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
    print(data)
	
    b_and_cname = {}
	
    # Iterating through the json
    # list
    for i in data['Annotations']:
        cname = i["classname"]
        bbox = i["BoundingBox"]
        if cname == "face_with_mask" or cname == "face_no_mask" or cname == "face_with_mask_incorrect" or cname == "face_other_covering" or cname == 'mask_colorful' or cname == 'mask_surgical':
            if cname == "face_other_covering":
                b_and_cname[str(bbox)] = "face_no_mask"
            else:
                b_and_cname[str(bbox)] = cname

    f.close()
    return b_and_cname

def rewrite_json_file(dictionary, new_filename):
	
    # Serializing json 
    json_object = json.dumps(dictionary, indent = len(dictionary))
	
    # Writing to sample.json
    with open(new_filename, "w") as outfile:
        outfile.write(json_object)

old_path = 'dataset/Medical Mask/old_annotations'
new_path = 'dataset/Medical Mask/annotations_more_mask_classes'

if not os.path.exists(new_path):
    os.makedirs(new_path)

dir_list = os.listdir(old_path)

for i in dir_list:
    old_filename = old_path + '/' + i

    # if images directory already converted to jpeg format
    image_id = i[:4]
    new_filename = new_path + '/' + image_id + '.jpeg.json'
    # if still in original image format
    #new_filename = new_path + '/' + i
    rewrite_json_file(readAnnotations(old_filename), new_filename)
