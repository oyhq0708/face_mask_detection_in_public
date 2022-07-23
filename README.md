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
YOLOv5 requires a special format of annotations, so we provide scripts in `data_preprocessing` folder to process the data. First run `rewrite_annotations.py`, then `redistribute_data.py`, finally `generate_txt_annotations.py`. Note for each script the paths need to be changed.

## train
training with original YOLOv5 architecture, run `python train.py --img 640 --batch 16 --data mask.yaml --weights yolov5l.pt --hyp data/hyps/hyp_mask.yaml`  
training with transformer, mobilenet or shufflenet structure, specify the configuration yaml file in `models/transformers` or `models/mobilenet_shufflenet`. One example is `python train.py --img 640 --batch 16 --data mask.yaml --weights yolov5l.pt --hyp data/hyps/hyp_mask.yaml --cfg models/transformers/yolov5l-transformer.yaml`  

## detect


## demo

## modified and self-created files
### modified files
`train.py`  
`utils/plots.py`  
`utils/loss.py`  
### created files
`data/hyps/hyp_mask.yaml`  
`data/mask.yaml`  
`data/more_mask_classes.yaml`  
`data_preprocessing/rewrite_annotations.py`  
`data_preprocessing/redistribute_data.py`  
`data_preprocessing/generate_txt_annotations.py`  
`count_labels.py`  
`models/transformers/yolov5l-transformer.yaml`
`models/mobilenet_shufflenet/
`demo_raw_videos` folder
