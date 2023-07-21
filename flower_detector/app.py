from fastapi import FastAPI, UploadFile, File

app = FastAPI()


@app.get('/')
def home():
    return {'Hello' : 'Flowery'}

@app.post('/flower_detec')
async def flower_detec(image : UploadFile = File(...)):
    
    img_size = len(await image.read())
    
    
    return {'img_size' : img_size }