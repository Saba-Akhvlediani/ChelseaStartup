# DEFINES HOW DATA IS RECEIVED FROM CLIENTS AND RETURNED IN RESPONSES
from pydantic import BaseModel,EmailStr
from .models import ServiceType



class InstructorBase(BaseModel):
    id: int
    username: str
    fullname: str | None = None
    gmail: EmailStr
    mobile_phone: int
    city: str
    category: str | None=None
    service_type: ServiceType
    experience: int
    bio: str
    min_salary: float | None=None
    max_salary: float | None=None

class InstructorCreate(InstructorBase):
    password: str
    photo_path: str

class Instructor(InstructorBase):
    id: int
    photo_path: str

