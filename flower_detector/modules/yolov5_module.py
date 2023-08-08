import torch
from PIL import Image

model = torch.hub.load('ultralytics/yolov5', 'custom', path='./modules/main_5_9.pt', force_reload=True, trust_repo=True)