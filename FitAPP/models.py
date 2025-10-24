# DEFINES HOW DATA IS STORED IN THE DATABASE

from sqlalchemy import Column,Integer,String,Float,Text,Enum as SQLEnum
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
    fullname = Column(String)
    gmail = Column(String,unique=True,index=True,nullable=False)
    mobile_phone = Column(Integer,nullable=False)
    city = Column(String,nullable=False)
    category = Column(String)
    experience = Column(Integer,nullable=False)
    service_type = Column(SQLEnum(ServiceType, native_enum=False), nullable=False)
    bio = Column(Text,nullable=False)
    photo_path = Column(String,nullable=False)
    min_salary = Column(Float,default=0)
    max_salary = Column(Float,default=0)


