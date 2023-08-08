from fastapi import FastAPI, UploadFile, UploadFile, Request
from io import BytesIO
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from modules.yolov5_module import model
from PIL import Image

import os, sys, shutil
sys.path.append(os.path.abspath('..'))

from db_session import SessionLocal


app = FastAPI()
templates = Jinja2Templates(directory='./templates')
app.mount('/detec_img', StaticFiles(directory='./detec_img'), name = 'detec_img')

@app.get('/')
def home():
    return {'Hello' : 'Flowery'}


@app.get('/flower_detec')
def flower_detec_page(request: Request):
    
    return templates.TemplateResponse('yolo.html', {'request' : request})

@app.post('/flower_detec')
async def flower_detec(request: Request, image : UploadFile = UploadFile(...)):
    image_data = await image.read()
    
    img_name = 'image0.jpg'
    
    img = Image.open(BytesIO(image_data))
    result = model(img)
    result.save()
    
    shutil.move(f'./runs/detect/exp/{img_name}', f'./detec_img/{img_name}')
    os.removedirs('./runs/detect/exp')
    
    image_path = f'http://t0922.p.ssafy.io:8001/detec_img/{img_name}'
    
    return templates.TemplateResponse('yolo.html', {'request': request, 'image_path' : image_path})