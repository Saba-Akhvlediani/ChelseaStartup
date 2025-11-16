# DEFINES HOW DATA IS STORED IN THE DATABASE

from sqlalchemy import Column,DateTime,Boolean,Integer,String,Float,Text,Enum as SQLEnum
from datetime import datetime
from enum import Enum as PYenum
from .database import Base

class ServiceType(str, PYenum):
    online = "დისტანციური"
    gym = "დარბაზი"
    home = "სახლში მისვლა"
    hybrid = "ჰიბრიდული"

class FitInstructorsTable(Base):
    __tablename__ = "Fitness_Instructors"

    id = Column(Integer,primary_key=True,index=True)
    username = Column(String,index=True,nullable=False)
    password = Column(String)
    fullname = Column(String)
    gmail = Column(String,unique=True,index=True,nullable=False)
    mobile_phone = Column(String,nullable=False)
    city = Column(String,nullable=False)
    address = Column(String,nullable=False)
    latitude = Column(Float,nullable=False)
    longitude = Column(Float,nullable=False)
    category = Column(String)
    experience = Column(Integer,nullable=False)
    service_type = Column(SQLEnum(ServiceType, native_enum=False), nullable=False)
    bio = Column(Text,nullable=False)
    photo_path = Column(String,nullable=False)
    min_salary = Column(Float,default=0)
    max_salary = Column(Float,default=0)
    rating = Column(Float,default=0)
    total_reviews = Column(Integer,default=0)
    available = Column(Boolean,index=True,default=True)
    is_verified = Column(Boolean,index=True,default=False)
    created_at = Column(DateTime,default=datetime.utcnow)
    updated_at = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)



# kvelafers gavasworeb instructorebis bazashi tu ramea mnishvnelovani dasamatebeli davamateb da mere shevqmni amas
# class FitCostumersTable(Base):
#     id = Column(Integer,primary_key=True,index=True)
#     username = Column(String,nullable=False,index=True)
#     fullname = Column(String,nullable=False,index=True)
#
