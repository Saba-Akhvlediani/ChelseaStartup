# Fastapi app and routes

from fastapi import FastAPI, Depends,UploadFile,File,Form,HTTPException,status
from . import models,schemas,crud
from sqlalchemy.orm import Session
from .database import get_db,Base,engine
from pathlib import Path

#create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fitness instructors API")

#create uploads directory
# UPLOAD_DIR = Path("uploads")
# UPLOAD_DIR.mkdir(exist_ok=True)


@app.post("/instructors/",response_model=schemas.Instructor,status_code=status.HTTP_201_CREATED)
async def create_fit_instructor(instructor: schemas.InstructorCreate, db: Session = Depends(get_db)):
    db_instructor = crud.get_fit_instructor_by_name(instructor.username,db)
    db_instructor_gmail = crud.get_fit_instructor_by_gmail(instructor.gmail,db)
    if db_instructor or db_instructor_gmail:
        raise HTTPException(status_code=400, detail="username or gmail already exist")
    return crud.create_instructor(instructor,db)


@app.get("/instructors/{instructor_id}",response_model=schemas.Instructor,status_code=status.HTTP_200_OK)
async def get_instructor_by_id(instructor_id: int, db: Session=Depends(get_db)):
    db_instructor = crud.get_fit_instructor_by_id(instructor_id,db)
    if db_instructor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="can't find instructor by that ID")
    return db_instructor
