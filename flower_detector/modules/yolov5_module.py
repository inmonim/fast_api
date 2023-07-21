import torch
from PIL import Image

model = torch.hub.load('ultralytics/yolov5', 'custom', path='main_5_9.pt', force_reload=True, trust_repo=True)

img = Image.open('../test_img/rose.jpg')

result = model(img)



print(result.xywh)