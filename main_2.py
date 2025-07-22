from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from fastapi import FastAPI, Depends
from pydantic import BaseModel

url="mysql+pymysql://asmitha:asmitha2003@localhost/mydb"

engine=create_engine(url)

Base=declarative_base()

class Student(Base):
    __tablename__='students'
    id=Column(Integer, primary_key=True)
    name=Column(String(50))
    age=Column(Integer)

Base.metadata.create_all(bind=engine)

#SessionLocal=sessionmaker(bind=engine)

# session=SessionLocal()

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    session=SessionLocal()
    try:
        yield session
    finally:
        session.close()

#FastAPI Code

app=FastAPI()

@app.get("/")
def Welcome():
    return "Welcome to FastAPI with MySQL"

class StudentCreate(BaseModel):
    name:str
    age: int

