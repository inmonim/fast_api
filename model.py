from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    password = Column(String)
    
class NlpLog(Base):
    __tablename__ = 'nlp_log'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sentence = Column(String)
    user_id = Column(Integer)