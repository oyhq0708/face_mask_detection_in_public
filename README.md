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
