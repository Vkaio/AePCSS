from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models.base import Base

user='dev'
password='password'
host='localhost'
database='dbtest'
db_url = f'mysql+mysqlconnector://{user}:{password}@{host}/{database}'

engine = create_engine(db_url)

def init_db():
    Base.metadata.create_all(engine)

db_session = sessionmaker(bind=engine)