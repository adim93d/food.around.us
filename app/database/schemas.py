from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


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


class UserPlantCreate(BaseModel):
    user_id: int
    plant_id: int
    image: Optional[str] = None
    date: Optional[datetime] = None
    description: Optional[str] = None


class UserPlantResponse(BaseModel):
    id: int
    user_id: int
    plant_id: int
    image: Optional[str]
    date: datetime
    description: Optional[str]

    class Config:
        from_attributes = True


class RecipeCreate(BaseModel):
    name: str
    content: str


class RecipeResponse(BaseModel):
    id : int
    name : str
    content: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
