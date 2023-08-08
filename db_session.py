from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import yaml

import os

with open(os.path.dirname(os.path.abspath(__file__))+'/config.yaml', 'r') as cf:
    config = yaml.safe_load(cf)

db_host = config['db']['host']
db_port = config['db']['port']
db_username = config['db']['username']
db_password = config['db']['password']
db_database = config['db']['database']

DB_URL = f'mysql+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_database}'
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def test_connect():
    
    from model import User
    
    with SessionLocal() as db:
        test_user = db.query(User).filter(User.id == 1).first()
    print(test_user.name)

test_connect()