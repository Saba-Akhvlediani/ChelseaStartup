# WRITE ALL DATABASE LOGIC SEPERATED FROM API ENDPOINTS

from . import models,schemas
from .database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends,status,HTTPException
from passlib.context import CryptContext
from pathlib import Path
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")


def hash_password(password):
    return pwd_context.hash(password)


def get_fit_instructor_by_id(instructor_id: int, db: Session=Depends(get_db)):
    return db.query(models.FitInstructorsTable).filter(models.FitInstructorsTable.id==instructor_id).first()


def get_fit_instructor_by_name(instructor_username: str, db: Session=Depends(get_db)):
    return db.query(models.FitInstructorsTable).filter(models.FitInstructorsTable.username==instructor_username).first()


def get_fit_instructor_by_gmail(instructor_gmail: str, db: Session=Depends(get_db)):
    return db.query(models.FitInstructorsTable).filter(models.FitInstructorsTable.gmail==instructor_gmail).first()


def create_instructor(instructor: schemas.InstructorCreate, photo_path: str, db: Session=Depends(get_db)):
    hashed_password = hash_password(instructor.password)
    db_instructor = models.FitInstructorsTable(username=instructor.username,
                                               password=hashed_password,
                                               fullname=instructor.fullname,
                                               gmail=instructor.gmail,
                                               mobile_phone=instructor.mobile_phone,
                                               city=instructor.city,
                                               category=instructor.category,
                                               experience=instructor.experience,
                                               service_type=instructor.service_type,
                                               bio=instructor.bio,
                                               photo_path=photo_path,
                                               min_salary=instructor.min_salary,
                                               max_salary=instructor.max_salary)

    db.add(db_instructor)
    db.commit()
    db.refresh(db_instructor)
    return db_instructor



def update_instructor(instructor_id: int, instructor_update: schemas.InstructorUpdate, db: Session=Depends(get_db)):

    db_instructor = get_fit_instructor_by_id(instructor_id,db)
    if not db_instructor:
        return None

    update_data = instructor_update.dict(exclude_unset=True,exclude_none=True)
    for key,value in update_data.items():
        if value is not None:
            if key=="password":
                setattr(db_instructor,key,hash_password(value))
            else:
                setattr(db_instructor,key,value)

    db.commit()
    db.refresh(db_instructor)
    return db_instructor



def update_instructor_photo(instructor_id: int, new_photo_path: str, db: Session=Depends(get_db)):

    db_instructor = get_fit_instructor_by_id(instructor_id,db)
    if not db_instructor:
        return None

    if db_instructor.photo_path:
        old_path = Path(db_instructor.photo_path)
        if old_path.exists():
            old_path.unlink()

    db_instructor.photo_path = new_photo_path

    db.commit()
    db.refresh(db_instructor)
    return db_instructor
