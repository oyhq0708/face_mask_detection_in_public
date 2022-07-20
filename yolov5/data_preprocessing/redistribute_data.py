import os
from shutil import copy2
from PIL import Image 
import random
import json
import ast

base_path = 'dataset/Medical Mask/new_more_mask_classes' #change path
annotations_path = 'dataset/Medical Mask/more_mask_classes_annotations'
images_path = 'dataset/Medical Mask/images' #change path
dir_list = os.listdir(images_path)
new_annotations_path = base_path + 'redistributed_train_annotations'
new_images_path = base_path + 'redistributed_train_images'
leaveout_annotations_path = base_path + 'redistributed_leaveout_annotations'
leaveout_images_path = base_path + 'redistributed_leaveout_images'
path_list = [new_annotations_path, new_images_path, leaveout_annotations_path, leaveout_images_path]
for p in path_list:
    if not os.path.exists(p):
        os.makedirs(p)

image_id = 0
for i in dir_list:
    im = Image.open(images_path + '/' + i)
    annotation_filename = annotations_path + '/' + i + '.json'
    f = open(annotation_filename)
    data = json.load(f)
    has_incorrect_class = False
    for bbox in data:
        class_to_category = {'face_with_mask': 0, 'face_no_mask': 1, 'face_with_mask_incorrect': 2, 'mask_colorful': 3, 'mask_surgical': 4}
        cl = data[bbox]
        category_id = class_to_category[cl]
        if category_id == 2: #or random.random() < 0.2: # face_with_mask_incorrect class, need more of this class, OR just crop some random bounding boxs for face_with_mask and face_no_mask classes
            incorrect_save_images_path = new_images_path
            incorrect_save_annotations_path = new_annotations_path

            print('face_with_mask_incorrect class')
            print('image name is ', i)
            has_incorrect_class = True
            im = Image.open(images_path + '/' + i)
            image_width, image_height = im.size
            bbox_list = ast.literal_eval(bbox) #[xmin, ymin, xmax, ymax]
            [xmin, ymin, xmax, ymax] = bbox_list
            bbox_length = xmax - xmin
            bbox_height = ymax - ymin
            # copy entire image
            if bbox_length > 0 and bbox_height > 0 and category_id == 2: # some bbox has 0 length and height
                print('{:04d}'.format(image_id))

                if random.random() >= 0.85:
                    incorrect_save_images_path = leaveout_images_path
                    incorrect_save_annotations_path = leaveout_annotations_path 
                    im.save(incorrect_save_images_path + '/' + '{:04d}'.format(image_id) + '.jpeg')
                    copy2(annotation_filename, incorrect_save_annotations_path + '/' + '{:04d}'.format(image_id) + '.jpeg.json')
                    image_id += 1
                    break # only put original image with face_with_mask_incorrect in leaveout folder, skip the remaining cropping, rotating and flipping part

                im.save(incorrect_save_images_path + '/' + '{:04d}'.format(image_id) + '.jpeg')
                copy2(annotation_filename, incorrect_save_annotations_path + '/' + '{:04d}'.format(image_id) + '.jpeg.json')
                image_id += 1
            else:
                continue

            # crop
            im_crop = im.crop((xmin, ymin, xmax, ymax))
            crop_dict = {}
            crop_bbox_list = [0, 0, bbox_length, bbox_height]
            crop_dict[str(crop_bbox_list)] = cl
            crop_json_object = json.dumps(crop_dict, indent = len(crop_dict))
            im_crop.save(incorrect_save_images_path + '/' + '{:04d}'.format(image_id) + '.jpeg')
            with open(incorrect_save_annotations_path + '/' + '{:04d}'.format(image_id) + '.jpeg.json', "w") as outfile:
                outfile.write(crop_json_object)
            image_id += 1

            # rotate to different degrees
            degree_list = [15, 30, 45, 60, 90, 150, 210, 270, 300, 315, 330, 345]
            for degree in degree_list:
                im_rotate = im_crop.rotate(degree, expand=True)
                im_rotate_length, im_rotate_height = im_rotate.size
                rotate_dict = {}
                rotate_bbox_list = [0, 0, im_rotate_length, im_rotate_height]
                rotate_dict[str(rotate_bbox_list)] = cl
                rotate_json_object = json.dumps(rotate_dict, indent = len(rotate_dict))
                im_rotate.save(incorrect_save_images_path + '/' + '{:04d}'.format(image_id) + '.jpeg')
                with open(incorrect_save_annotations_path + '/' + '{:04d}'.format(image_id) + '.jpeg.json', "w") as outfile:
                    outfile.write(rotate_json_object)
                image_id += 1

            # flip left right
            im_flip_lr = im_crop.transpose(method=Image.Transpose.FLIP_LEFT_RIGHT)
            im_flip_lr.save(incorrect_save_images_path + '/' + '{:04d}'.format(image_id) + '.jpeg')
            with open(incorrect_save_annotations_path + '/' + '{:04d}'.format(image_id) + '.jpeg.json', "w") as outfile:
                outfile.write(crop_json_object)
            image_id += 1
            '''
            # flip top bottom
            im_flip_tb = im_crop.transpose(method=Image.Transpose.FLIP_TOP_BOTTOM)
            im_flip_tb.save(new_images_path + '/' + str(image_id) + '.jpeg')
            with open(new_annotations_path + '/' + str(image_id) + '.jpeg.json', "w") as outfile:
                outfile.write(crop_json_object)
            image_id += 1
            '''
            if category_id == 2:
                break
    if not has_incorrect_class:
        # randomly decide whether this image will be copied to the redistributed data folder
        if random.random() < 0.5: # 50% chance this image will be included
            im.save(new_images_path + '/' + '{:04d}'.format(image_id) + '.jpeg')
            copy2(annotation_filename, new_annotations_path + '/' + '{:04d}'.format(image_id) + '.jpeg.json')
            image_id += 1
        
        else: 
            im.save(leaveout_images_path + '/' + '{:04d}'.format(image_id) + '.jpeg')
            copy2(annotation_filename, leaveout_annotations_path + '/' + '{:04d}'.format(image_id) + '.jpeg.json')
            image_id += 1
        
