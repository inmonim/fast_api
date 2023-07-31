from fastapi import FastAPI, HTTPException

import os, sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from db_session import SessionLocal
from model import User


app = FastAPI()

@app.get('/')
def homepage():
    return {'hello' : 'world'}

@app.get('/{user_id}')
def get_user_id(user_id):
    with SessionLocal() as db:
        user = db.query(User).filter(User.id == user_id).first()
        
        if user is None:
            raise HTTPException(status_code=404, detail='User not Found')
        
    return {'user_name' : user.name}