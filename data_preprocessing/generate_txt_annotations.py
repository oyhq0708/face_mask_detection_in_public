import json
import os
import ast
from PIL import Image
from shutil import copy2

def generate_txt_annotations(trainOrTest):
    base_path = '../dataset/Medical Mask/new_more_mask_classes_redistributed_' #change path, but need to keep 'redistributed_'
    images_path = base_path + trainOrTest + '_images/'
    annotations_path = base_path + trainOrTest + '_annotations/'
    new_images_path = base_path + trainOrTest + '/images/'
    new_annotations_path = base_path + trainOrTest + '/labels/'
    if not os.path.exists(new_images_path):
        os.makedirs(new_images_path)
    if not os.path.exists(new_annotations_path):
        os.makedirs(new_annotations_path)
    dir_list = os.listdir(images_path)
    for i in dir_list:
        image_filename = images_path + i
        annotation_filename = annotations_path + i + '.json'
        copy2(image_filename, new_images_path)
        im = Image.open(image_filename)
        image_width, image_height = im.size
        image_id = i[:4] # get the number from the filename

        f = open(annotation_filename)
        data = json.load(f)
        if data is None:
            print('None')
            continue
        new_data = ''
        #print(data)
        for bbox in data:
            bbox_list = ast.literal_eval(bbox) #[xmin, ymin, xmax, ymax]
            [xmin, ymin, xmax, ymax] = bbox_list
            bbox_width = 1.0 * (xmax - xmin) / image_width
            bbox_height = 1.0 * (ymax - ymin) / image_height
            x_center = 1.0 * (xmin + (xmax - xmin) / 2) / image_width
            y_center = 1.0 * (ymin + (ymax - ymin) / 2) / image_height
            class_to_category = {'face_with_mask': 0, 'face_no_mask': 1, 'face_with_mask_incorrect': 2, 'mask_colorful': 3, 'mask_surgical': 4}
            cl = data[bbox]
            category_id = class_to_category[cl]
            new_data += str(category_id) + ' ' + str(round(x_center, 6)) + ' ' + str(round(y_center, 6)) + ' ' + str(round(bbox_width, 6)) + ' ' + str(round(bbox_height, 6)) + '\n'

        new_annotation_filename = new_annotations_path + image_id + '.txt'
        #print(new_data)
        with open(new_annotation_filename, 'w') as outfile:
            outfile.write(new_data)

if __name__ == '__main__':
    generate_txt_annotations('leaveout')
    generate_txt_annotations('train')
    #generate_txt_annotations('val')
    #generate_txt_annotations('test')
