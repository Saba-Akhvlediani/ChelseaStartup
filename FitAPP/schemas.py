# DEFINES HOW DATA IS RECEIVED FROM CLIENTS AND RETURNED IN RESPONSES
from pydantic import BaseModel,EmailStr
from .models import ServiceType



class InstructorBase(BaseModel):
    # id: int
    username: str
    fullname: str | None=None
    gmail: EmailStr
    mobile_phone: str
    city: str
    category: str | None=None
    service_type: ServiceType
    experience: int
    bio: str
    min_salary: float | None=None
    max_salary: float | None=None

class InstructorUpdate(BaseModel):
    username: str | None=None
    password: str | None=None
    fullname: str | None=None
    gmail: EmailStr | None=None
    mobile_phone: str | None=None
    city: str | None=None
    category: str | None = None
    service_type: ServiceType | None=None
    experience: int | None=None
    bio: str | None=None
    min_salary: float | None = None
    max_salary: float | None = None


    class Config:
        # This helps Pydantic understand partial updates
        validate_assignment = True



class InstructorCreate(InstructorBase):
    password: str

class Instructor(InstructorBase):
    id: int
    photo_path: str

