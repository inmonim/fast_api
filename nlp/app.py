from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import matplotlib.pyplot as plt

import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from db_session import SessionLocal
from model import NlpLog


from modules.KoBERT_module import load_nlp_model, emotion_predict

app = FastAPI()


if not os.path.isdir('plt_tmp'):
    os.mkdir('plt_tmp')

app.mount("/plt_img", StaticFiles(directory="./plt_tmp"), name='plt_img')

templates = Jinja2Templates(directory='./templates')

model = load_nlp_model()


@app.get('/')
def home():
    return {'Hello': 'NLP'}

@app.get('/get_emotion')
def ep2(request: Request):
    return templates.TemplateResponse('nlp.html', {'request': request})


@app.post('/get_emotion')
async def get_emotion(request: Request):
    form_data = await request.form()
    sentence = form_data['sentence']
    result = emotion_predict(model, sentence)
    
    with SessionLocal() as db:
        log = NlpLog()
        log.sentence = sentence
        log.user_id = 1
        db.add(log)
        db.commit()
    
    ratio, labels = [], []
    for i in result:
        if max(i[1],0):
            ratio.append(i[1])
            labels.append(i[0])
    
    plt.pie(ratio, labels=labels, autopct='%.1f%%')
    image_path = f'./plt_tmp/{sentence}.png'
    plt.savefig(image_path)
    image_path = f'http://t0922.p.ssafy.io:8000/plt_img/{sentence}.png'
    plt.close()
    
    return templates.TemplateResponse('nlp.html', {'request': request, 'result': result, 'image_path':image_path})