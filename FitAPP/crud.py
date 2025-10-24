# WRITE ALL DATABASE LOGIC SEPERATED FROM API ENDPOINTS

from . import models,schemas
from .database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends,status,HTTPException


def get_fit_instructor_by_id(instructor_id: int, db: Session=Depends(get_db)):
    return db.query(models.FitInstructorsTable).filter(models.FitInstructorsTable.id==instructor_id).first()

def get_fit_instructor_by_name(instructor_username: str, db: Session=Depends(get_db)):
    return db.query(models.FitInstructorsTable).filter(models.FitInstructorsTable.username==instructor_username).first()

def get_fit_instructor_by_gmail(instructor_gmail: str, db: Session=Depends(get_db)):
    return db.query(models.FitInstructorsTable).filter(models.FitInstructorsTable.gmail==instructor_gmail).first()


def create_instructor(instructor: schemas.InstructorCreate, db: Session=Depends(get_db)):
    db_instructor = models.FitInstructorsTable(username=instructor.username,
                                               fullname=instructor.fullname,
                                               gmail=instructor.gmail,
                                               mobile_phone=instructor.mobile_phone,
                                               city=instructor.city,
                                               category=instructor.category,
                                               experience=instructor.experience,
                                               service_type=instructor.service_type,
                                               bio=instructor.bio,
                                               photo_path=instructor.photo_path,
                                               min_salary=instructor.min_salary,
                                               max_salary=instructor.max_salary)
    db.add(db_instructor)
    db.commit()
    db.refresh(db_instructor)
    return db_instructor