# schemas.py
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


class PlantCreate(BaseModel):
    scientific_name : str
    family: str
    is_edible: bool


class PlantResponse(BaseModel):
    id : int
    scientific_name : str
    family: str
    is_edible: bool



