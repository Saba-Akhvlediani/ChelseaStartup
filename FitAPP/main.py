# Fastapi app and routes

from fastapi import FastAPI, Depends,UploadFile,File,Form,HTTPException,status,Query
from fastapi.staticfiles import StaticFiles
from . import models,schemas,crud
from sqlalchemy.orm import Session
from .database import get_db,Base,engine
from pydantic import EmailStr
from pathlib import Path
from typing import Optional, Unpack,List
import shutil
import uuid

#create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fitness instructors API")

#create uploads directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

async def save_photo(photo: UploadFile, username: str):
    #validate file type
    if not photo.content_type.startswith("image/"):
        raise HTTPException(status_code=400,detail="File must be an image jpg,png, etc.")

    #validate file size (5mb max)
    photo.file.seek(0,2)
    file_size = photo.file.tell()
    photo.file.seek(0)

    if file_size > 5 * 1024 * 1024:
        raise HTTPException(status_code=400,detail="File size must be less than 5 mb")

    #create unique filename
    file_extension = photo.filename.split(".")[-1]
    unique_filename = f"{username}_{uuid.uuid4().hex[:8]}.{file_extension}"
    file_path = UPLOAD_DIR / unique_filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)

    return str(file_path)


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float):
    """
        Calculate distance between two points using Haversine formula.
        Returns distance in kilometers.
    """
    R = 6371  #earth's radius in kilometers

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a),math.sqrt(1 - a))
    distance = R * c
    return distance



@app.post("/instructors/",response_model=schemas.Instructor,status_code=201)
async def create_fit_instructor(
        username: str = Form(...),
        password: str = Form(...),
        fullname: Optional[str] = Form(None),
        gmail: EmailStr = Form(...),
        mobile_phone: str = Form(...),
        city: str = Form(...),
        address: str = Form(...),
        latitude: float = Form(...),
        longitude: float = Form(...),
        category: Optional[str] = Form(None),
        service_type: str = Form(...),
        experience: int = Form(...),
        bio: str = Form(...),
        min_salary: Optional[float] = Form(None),
        max_salary: Optional[float] = Form(None),
        photo: UploadFile = File(...),
        db: Session = Depends(get_db)):

        db_instructor = crud.get_fit_instructor_by_name(username,db)
        db_instructor_gmail = crud.get_fit_instructor_by_gmail(gmail,db)

        if db_instructor:
            raise HTTPException(status_code=400,detail="Username already exists")

        if db_instructor_gmail:
            raise HTTPException(status_code=400,detail="Email already registered")

        if not (-90 <= latitude <= 90):
            raise HTTPException(status_code=400, detail="latitude must be between -90 and 90")
        if not (-180 <= longitude <= 180):
            raise HTTPException(status_code=400, detail="longitude must be between -180 and 180")

        photo_path = await save_photo(photo,username)

        fit_instructor_data = schemas.InstructorCreate(username=username,
                                                       password=password,
                                                       fullname=fullname,
                                                       gmail=gmail,
                                                       mobile_phone=mobile_phone,
                                                       city=city,
                                                       address=address,
                                                       latitude=latitude,
                                                       longitude=longitude,
                                                       category=category,
                                                       service_type=service_type,
                                                       experience=experience,
                                                       bio=bio,
                                                       min_salary=min_salary,
                                                       max_salary=max_salary)

        return crud.create_instructor(fit_instructor_data,photo_path,db)


@app.put("/instructors/{instructor_id}",response_model=schemas.Instructor,status_code=status.HTTP_200_OK)
async def update_instructor_data(instructor_id: int, updated_data: schemas.InstructorUpdate, db: Session=Depends(get_db)):

    db_instructor = crud.get_fit_instructor_by_id(instructor_id,db)
    if not db_instructor:
        raise HTTPException(status_code=404,detail="Can't find instructor with this ID")

    db_instructor_gmail = crud.get_fit_instructor_by_gmail(updated_data.gmail,db)
    if db_instructor_gmail and db_instructor_gmail.id != instructor_id:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_instructor_username = crud.get_fit_instructor_by_name(updated_data.username,db)
    if db_instructor_username and db_instructor_username.id != instructor_id:
        raise HTTPException(status_code=400,detail="Username already exists")

    if updated_data.latitude is not None and not (-90 <= updated_data.latitude <= 90):
        raise HTTPException(status_code=400, detail="Latitude must be between -90 and 90")
    if updated_data.longitude is not None and not (-180 <= updated_data.longitude <= 180):
        raise HTTPException(status_code=400, detail="Longitude must be between -180 and 180")


    updated_instructor = crud.update_instructor(instructor_id,updated_data,db)

    return updated_instructor




@app.put("/instructors/{instructor_id}/photo",response_model=schemas.Instructor,status_code=200)
async def update_instructor_photo(instructor_id: int, new_photo: UploadFile=File(...), db: Session=Depends(get_db)):
    db_instructor = crud.get_fit_instructor_by_id(instructor_id,db)
    if not db_instructor:
        raise HTTPException(status_code=404,detail="Can't find instructor with this ID")

    if not new_photo or not new_photo.filename:
        raise HTTPException(status_code=400,detail="Photo is required!!!")

    new_photo_path = await save_photo(new_photo,db_instructor.username)
    updated_instructor_photo = crud.update_instructor_photo(instructor_id,new_photo_path,db)

    return updated_instructor_photo




@app.get("/instructors/{instructor_id}",response_model=schemas.Instructor,status_code=200)
async def get_instructor_by_id(instructor_id: int, db: Session=Depends(get_db)):
    db_instructor = crud.get_fit_instructor_by_id(instructor_id,db)
    if not db_instructor:
        raise HTTPException(status_code=404,detail="Can't find instructor with this ID")
    return db_instructor


@app.get("/instructors/",response_model=List[schemas.Instructor],status_code=200)
async def search_instructors(
        city: str | None = Query(None, description="Filter by city"),
        category: str | None = Query(None, description="Filter by category"),
        service_type: str | None = Query(None, description="Filter by service_type"),
        min_experience: int | None = Query(None, description="Minimum years of experience"),
        max_price: float | None = Query(None, description="Maximum price willing to pay"),
        latitude: float | None = Query(None, description="User's latitude for distance calculation"),
        longitude: float | None = Query(None, description="User's longitude for distance calculation"),
        max_distance: float | None = Query(None, description="Maximum distance in kilometers"),
        available_only: bool | None = Query(True, description="Show only available instructors"),
        db: Session = Depends(get_db)

):
    query = db.query(models.FitInstructorsTable)
    if city:
        query = query.filter(models.FitInstructorsTable.city == city)
    if category:
        query = query.filter(models.FitInstructorsTable.category == category)
    if service_type:
        query = query.filter(models.FitInstructorsTable.service_type == service_type)
    if min_experience:
        query = query.filter(models.FitInstructorsTable.experience >= min_experience)
    if max_price:
        query = query.filter(models.FitInstructorsTable.min_salary <= max_price)
    if available_only:
        query = query.filter(models.FitInstructorsTable.available == True)

    instructors = query.all()

    if latitude is not None and longitude is not None and max_distance is not None:
        filtered_instructors = []
        for instructor in instructors:
            distance = calculate_distance(latitude, longitude, instructor.latitude, instructors.longitude)
            if distance <= max_distance:
                filtered_instructors.append(instructor)
        instructors = filtered_instructors

    return instructors



@app.delete("/instructors/{instructor_id}",response_model=schemas.Instructor,status_code=200)
async def delete_instructor_by_id(instructor_id: int, db: Session=Depends(get_db)):
    db_instructor = crud.get_fit_instructor_by_id(instructor_id,db)
    if not db_instructor:
        raise HTTPException(status_code=404,detail="Can't find instructor with this ID ")

    delete_instructor = crud.delete_instructor(instructor_id,db)

    return delete_instructor