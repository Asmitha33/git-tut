from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from fastapi.responses import JSONResponse

url="mysql+pymysql://asmitha:asmitha2003@localhost/mydb"

engine=create_engine(url)

Base=declarative_base()

class Student(Base):
    __tablename__='students_1'
    id=Column(Integer, primary_key=True)
    first_name=Column(String(20))
    last_name=Column(String(20))
    age=Column(Integer)

Base.metadata.create_all(bind=engine)

SessionLoacl=sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    session=SessionLoacl()
    try:
        yield session
    finally:
        session.close()

app=FastAPI()

class studenCreate(BaseModel):
    first_name:str
    last_name:str
    age:int
    class Config:
        orm_mode = True

@app.get("/")
def welcome():
    return "Welcome to FastAPI + MySQL"

@app.post("/create_data/")
def create_student(student:studenCreate, session:Session=Depends(get_db)):
    new_student = Student(first_name=student.first_name, last_name=student.last_name, age=student.age)
    session.add(new_student)
    session.commit()
    return f"Student {new_student.first_name} {new_student.last_name} created successfully"

@app.get("/get_data/")
def get_student(session: Session=Depends(get_db)):
    students=session.query(Student).all()
    return students

@app.get("/get_data/{student_id}", response_model=studenCreate)
def get_student(student_id:int, session: Session=Depends(get_db)):
    students=session.query(Student).filter(Student.id==student_id).first()
    if not students:
        return JSONResponse(status_code=404, content={"message": f"Student with ID {student_id} not found. Please add a new student."})
    else:
        return students

@app.put("/update_data/")
def update_student(student_id: int, first_name:str, age: int, session:Session=Depends(get_db)):
    student=session.query(Student).filter(Student.id==student_id).first()
    if not student:
        return "Student not found"
    else:
        student.first_name=first_name
        session.commit()
        return f"student with {student_id} updated succesfully"
    
@app.delete("/delete_data/")
def delete_student(student_id: int, session: Session = Depends(get_db)):
    student=session.query(Student).filter(Student.id==student_id).first()
    if not student:
        return "Student not found"
    else:
        session.delete(student)
        session.commit()
        return f"student with {student_id} deleted succesfully"