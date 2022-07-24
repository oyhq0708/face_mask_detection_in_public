# face mask detection in public
HKU Capstone Project<br />
Mainly based on YOLOv5<br />

## dataset
info page: https://humansintheloop.org/mask-dataset-download/?submissionGuid=fa0fb79c-ddc2-4971-a284-2ce50774d9fd  
direct download link: https://mask-dataset.s3.eu-central-1.amazonaws.com/Medical+mask.zip  
This dataset has more than 6,000 images and provides annotations for 20 classes.
Our task is to classify whether an object is belonged to face_with_mask, face_no_mask, or face_with_mask_incorrect class.  
We consider faces covered by non-masks such as scarves as face_no_mask.

## preprocessing
YOLOv5 requires a special format of annotations, so we provide scripts in `data_preprocessing` folder to process the data. Simply run `python3 preprocessing.py` for basic 3 classes option, or `python3 preprocessing_more_mask_classes.py` for additional 2 mask type classes. Note for `data_preprocessing/preprocessing.py`, `data_preprocessing/preprocessing_more_mask_classes.py`, `data/mask.yaml` and `data/mask_more_classes.yaml` the paths need to be changed. 

## train
### for the basic 3 classes
training with original YOLOv5 architecture, run `python train.py --img 640 --batch 16 --data mask.yaml --weights yolov5l.pt --hyp data/hyps/hyp_mask.yaml`  
training with transformer, mobilenet or shufflenet structure, specify the configuration yaml file in `models/transformers` or `models/mobilenet_shufflenet`. One example is `python train.py --img 640 --batch 16 --data mask.yaml --weights yolov5l.pt --hyp data/hyps/hyp_mask.yaml --cfg models/transformers/yolov5l-transformer.yaml`  
### with 2 mask type classes
execute `python train.py --img 640 --batch 16 --data mask_more_classes.yaml --weights yolov5l.pt --hyp data/hyps/hyp_mask.yaml`

## trained paths that can be used to run validation and detection
download from https://drive.google.com/drive/folders/1j6IkElVvAPfFAob2qfBZa1T0A3T7NjXc?usp=sharing  
One is for the basic 3 classes, the other one is an advanced path that is able to detect the type of the mask. To run the advanced version, use `--data more_mask_classes.yaml` and prepare the dataset accordingly.

## validate
run `python val.py --img 640 --data mask.yaml --weights YOUR_TRAINED_PATH`  
see val.py for more information
## detect
run `python detect.py --weights YOUR_TRAINED_PATH --source YOUR_SOURCE`  
see detect.py for more information
## demo
demo1 on 3 basic classes (click to view)  
[![1_basic_classes](https://img.youtube.com/vi/2JLqEhV0sOc/0.jpg)](https://www.youtube.com/watch?v=2JLqEhV0sOc)  
(original video from https://www.bilibili.com/video/BV1zV411m7XF?spm_id_from=333.999.0.0&vd_source=0e7aa368809c558f3313adec21a3df56)  

demo2 on 3 basic classes (click to view)  
[![2_basic_classes](https://img.youtube.com/vi/uYrjUkY2ADs/0.jpg)](https://www.youtube.com/watch?v=uYrjUkY2ADs)  
(original video from https://youtu.be/tGkhfd2PuAY)  

demo1 on 3 basic classes plus 2 mask types (click to view)  
[![1_more_mask_classes](https://img.youtube.com/vi/kjj3JAXRwZQ/0.jpg)](https://www.youtube.com/watch?v=kjj3JAXRwZQ)  
(original video from https://www.bilibili.com/video/BV1zV411m7XF?spm_id_from=333.999.0.0&vd_source=0e7aa368809c558f3313adec21a3df56)  

demo2 on 3 basic classes plus 2 mask types (click to view)  
[![2_more_mask_classes](https://img.youtube.com/vi/J-NRoH5uk_o/0.jpg)](https://www.youtube.com/watch?v=J-NRoH5uk_o)  
(original video from https://youtu.be/tGkhfd2PuAY)  

## modified and self-created files
### modified files
`train.py`  
`utils/plots.py`  
`utils/loss.py`  
`models/yolo.py`
`models/common.py`

### created files
`data/hyps/hyp_mask.yaml`  
`data/mask.yaml`  
`data/more_mask_classes.yaml`  
`data_preprocessing/rewrite_annotations.py`  
`data_preprocessing/redistribute_data.py`  
`data_preprocessing/generate_txt_annotations.py`  
`data_preprocessing/count_labels.py`  
`data_preprocessing/preprocessing.py`  
`data_preprocessing/preprocessing_more_mask_classes.py`  
`models/transformers/yolov5l-transformer.yaml`  
`models/mobilenet_shufflenet/yolov5l-mobilenetv3.yaml`  
`models/mobilenet_shufflenet/yolov5l-shufflenet.yaml`  
`models/mobilenet_shufflenet/yolov5l-shufflenetv2-focus.yaml`  
`models/mobilenet_shufflenet/yolov5s+mobilenetv3.yaml`  
`models/mobilenet_shufflenet/yolov5s+shufflenet.yaml`  
`demo_raw_videos` folder
