from fastapi import FastAPI, HTTPException, Depends

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt import PyJWTError
from datetime import datetime, timedelta
from typing import Optional

import os, sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from db_session import SessionLocal
from model import User


SECRET_KEY = "eeeqwe"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")


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


@app.post('/login')
async def login(form_data : OAuth2PasswordRequestForm = Depends()):
    with SessionLocal() as db:
        user = db.query(User).get(User.name == form_data.user)
        
        if user is None or user['password'] != form_data.password:
            raise HTTPException(status_code=401, detail='Access Denied')
        
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user["username"]}, expires_delta=access_token_expires)
    
    return {"access_token": access_token, "token_type": "bearer"}