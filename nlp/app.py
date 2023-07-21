from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import matplotlib.pyplot as plt

from modules.KoBERT_module import load_nlp_model, emotion_predict

app = FastAPI()

app.mount("/plt_img", StaticFiles(directory="./plt_tmp"), name='plt_img')

templates = Jinja2Templates(directory='./templates')

model = load_nlp_model()


@app.get('/')
def home():
    return {'Hello': 'World'}

@app.get('/get_emotion')
def ep2(request: Request):
    return templates.TemplateResponse('nlp.html', {'request': request})


@app.post('/get_emotion')
async def get_emotion(request: Request):
    form_data = await request.form()
    sentence = form_data['sentence']
    print(sentence)
    result = emotion_predict(model, sentence)
    
    ratio, labels = [], []
    for i in result:
        if max(i[1],0):
            ratio.append(i[1])
            labels.append(i[0])
    
    plt.pie(ratio, labels=labels, autopct='%.1f%%')
    image_path = f'./plt_tmp/{sentence}.png'
    plt.savefig(image_path)
    image_path = f'http://127.0.0.1:8000/plt_img/{sentence}.png'
    plt.close()
    
    return templates.TemplateResponse('nlp.html', {'request': request, 'result': result, 'image_path':image_path})