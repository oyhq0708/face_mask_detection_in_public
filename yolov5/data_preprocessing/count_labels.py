import os
from shutil import copy2
from PIL import Image 
import random
import json
import ast

base_path = 'dataset/Medical Mask/redistributed_train_' #change path
annotations_path = base_path + 'annotations'#'annotations'
images_path = base_path + 'images'
dir_list = os.listdir(images_path)

num_face_with_mask = 0
num_face_no_mask = 0
num_face_with_mask_incorrect = 0
num_mask_colorful = 0
num_mask_surgical = 0

for i in dir_list:
    annotation_filename = annotations_path + '/' + i + '.json'
    f = open(annotation_filename)
    data = json.load(f)

    for bbox in data:
        class_to_category = {'face_with_mask': 0, 'face_no_mask': 1, 'face_with_mask_incorrect': 2, 'mask_colorful': 3, 'mask_surgical': 4}
        cl = data[bbox]
        category_id = class_to_category[cl]
        bbox_list = ast.literal_eval(bbox) #[xmin, ymin, xmax, ymax]
        [xmin, ymin, xmax, ymax] = bbox_list
        bbox_length = xmax - xmin
        bbox_height = ymax - ymin
        if bbox_length > 0 and bbox_height > 0:
            if category_id == 0:
                num_face_with_mask += 1
            elif category_id == 1:
                num_face_no_mask += 1
            elif category_id == 2:
                num_face_with_mask_incorrect += 1
            elif category_id == 3:
                num_mask_colorful += 1
            elif category_id == 4:
                num_mask_surgical += 1

print('num_face_with_mask = ', num_face_with_mask)
print('num_face_no_mask = ', num_face_no_mask)
print('num_face_with_mask_incorrect = ', num_face_with_mask_incorrect)
print('num_mask_colorful = ', num_mask_colorful)
print('num_mask_surgical = ', num_mask_surgical)
