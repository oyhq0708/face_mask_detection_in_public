import json
import os
import ast
from PIL import Image
from shutil import copy2
import random

class_to_category = {'face_with_mask': 0, 'face_no_mask': 1, 'face_with_mask_incorrect': 2}

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
        if cname == "face_with_mask" or cname == "face_no_mask" or cname == "face_with_mask_incorrect" or cname == "face_other_covering":
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


def generate_txt_annotations(trainOrTest):
    #txt_base_path = '../dataset/Medical Mask/new_more_mask_classes_redistributed_' #change path, but need to keep 'redistributed_'
    txt_images_path = redistributed_base_path + trainOrTest + '_images/'
    txt_annotations_path = redistributed_base_path + trainOrTest + '_annotations/'
    txt_new_images_path = redistributed_base_path + trainOrTest + '/images/'
    txt_new_annotations_path = redistributed_base_path + trainOrTest + '/labels/'
    if not os.path.exists(txt_new_images_path):
        os.makedirs(txt_new_images_path)
    if not os.path.exists(txt_new_annotations_path):
        os.makedirs(txt_new_annotations_path)
    txt_dir_list = os.listdir(txt_images_path)
    for i in txt_dir_list:
        image_filename = txt_images_path + i
        annotation_filename = txt_annotations_path + i + '.json'
        copy2(image_filename, txt_new_images_path)
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

            cl = data[bbox]
            category_id = class_to_category[cl]
            new_data += str(category_id) + ' ' + str(round(x_center, 6)) + ' ' + str(round(y_center, 6)) + ' ' + str(round(bbox_width, 6)) + ' ' + str(round(bbox_height, 6)) + '\n'

        new_annotation_filename = txt_new_annotations_path + image_id + '.txt'
        #print(new_data)
        with open(new_annotation_filename, 'w') as outfile:
            outfile.write(new_data)


base_path = '../../dataset_backup/Medical mask/Medical Mask/' # change this path
images_path = base_path + 'images'
old_annotations_path = base_path + 'annotations'
annotations_path = base_path + 'annotations_rewrite'
redistributed_base_path = base_path + 'redistributed_'
new_annotations_path = redistributed_base_path + 'train_annotations'
new_images_path = redistributed_base_path + 'train_images'
leaveout_annotations_path = redistributed_base_path + 'leaveout_annotations'
leaveout_images_path = redistributed_base_path + 'leaveout_images'
path_list = [annotations_path, new_annotations_path, new_images_path, leaveout_annotations_path, leaveout_images_path]

for p in path_list:
    if not os.path.exists(p):
        os.makedirs(p)

old_image_dir_list = os.listdir(images_path)
old_annotations_dir_list = os.listdir(old_annotations_path)


# only keep the classes we want, rewrite all annotations
for i in old_annotations_dir_list:
    old_filename = old_annotations_path + '/' + i

    # if images directory already converted to jpeg format
    image_id = i[:4]
    new_filename = annotations_path + '/' + image_id + '.jpeg.json'
    # if still in original image format
    #new_filename = new_path + '/' + i
    rewrite_json_file(readAnnotations(old_filename), new_filename)


# change everything to jpeg, during this process 7 images are thrown because they have same jpeg_filename
for i in old_image_dir_list:
    #print('i = ', i)
    image_id = i[:4]
    jpeg_filename = image_id + '.jpeg'
    #print('jpeg_filename = ', jpeg_filename)
    
    if i != jpeg_filename:
        #print('not same')
        im = Image.open(images_path + '/' + i)
        im.save(images_path + '/' + jpeg_filename)
        os.remove(images_path + '/' + i)
        #os.rename(annotations_path + '/' + i + '.json', annotations_path + '/' + jpeg_filename + '.json')


# redistribute data
dir_list = os.listdir(images_path)
image_id = 0
for i in dir_list:
    im = Image.open(images_path + '/' + i)
    annotation_filename = annotations_path + '/' + i + '.json'
    f = open(annotation_filename)
    data = json.load(f)
    has_incorrect_class = False
    for bbox in data:
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



# generate the txt files per YOLO requirements
generate_txt_annotations('leaveout')
generate_txt_annotations('train')

