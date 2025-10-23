from fastapi import FastAPI, Depends,UploadFile,File,Form,HTTPException
from . import models
from sqlachemy.orm Session
from pathlib import Path
from enum import Enum



app = FastAPI()

#create uploads directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# @app.post("/instructors/",response_model=models.FitInstructorsTable)
# async def create_fit_instructor()

class ServiceType(str, Enum):
    online = "დისტანციური"
    gym = "დარბაზი"
    home = "სახლში მისვლა"
    hybrid = "ჰიბრიდული"
