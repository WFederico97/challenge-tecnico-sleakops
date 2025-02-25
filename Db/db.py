import os
from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,Session

SQLALCHEMY_DATABASE_URL = os.getenv("URL_DB", "postgresql://postgres:postgres@localhost:5432/sleakops")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
session_local = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

def create_tables():
    Base.metadata.create_all(bind= engine)

def get_db() :
  db = session_local()
  try: 
    yield db
    db.commit()
  finally:
    db.close()

db_dependency = Annotated[ Session, Depends(get_db) ]