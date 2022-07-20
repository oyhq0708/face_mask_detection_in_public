import torch
import sys
import os
sys.path.append(os.getcwd())
from models.yolo import Model
from utils.torch_utils import EarlyStopping, ModelEMA, de_parallel, select_device
from utils.general import (LOGGER, check_amp, check_dataset, check_file, check_git_status, check_img_size,
                           check_requirements, check_suffix, check_version, check_yaml, colorstr, get_latest_run,
                           increment_path, init_seeds, intersect_dicts, labels_to_class_weights,
                           labels_to_image_weights, methods, one_cycle, print_args, print_mutation, strip_optimizer)

device = select_device('', batch_size=16)
ckpt = torch.load('yolov5l.pt', map_location='cpu')  # load checkpoint to CPU to avoid CUDA memory leak
model = Model('' or ckpt['model'].yaml, ch=3, nc=3, anchors=4).to(device)  # create
exclude = ['anchor'] if ('' or 4) and True else []  # exclude keys
csd = ckpt['model'].float().state_dict()  # checkpoint state_dict as FP32
csd = intersect_dicts(csd, model.state_dict(), exclude=exclude)  # intersect
model.load_state_dict(csd, strict=False)
torch.save(csd, 'yolov5l_statedict.pt')

