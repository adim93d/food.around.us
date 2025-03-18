from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database.models import UserPlant, User, Plant
from app.database.database import SessionLocal
from app.database.schemas import UserPlantCreate, UserPlantResponse
from app.api.routers.auth import get_current_user
from datetime import datetime

# All endpoints in this router require authentication
router = APIRouter(dependencies=[Depends(get_current_user)])


# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CREATE a user-plant relationship
@router.post("/", response_model=UserPlantResponse, tags=["User-Plants"])
def create_user_plant(user_plant: UserPlantCreate, db: Session = Depends(get_db)):
    # Check if the plant-user relationship already exists
    db_user_plant = db.query(UserPlant).filter(
        UserPlant.user_id == user_plant.user_id,
        UserPlant.plant_id == user_plant.plant_id
    ).first()

    if db_user_plant:
        raise HTTPException(status_code=400, detail="User already has this plant registered.")

    # Create new user-plant relationship
    new_user_plant = UserPlant(
        user_id=user_plant.user_id,
        plant_id=user_plant.plant_id,
        image=user_plant.image,
        date=user_plant.date or datetime.utcnow(),
        description=user_plant.description
    )

    db.add(new_user_plant)
    db.commit()
    db.refresh(new_user_plant)

    return new_user_plant


# READ all user-plant relationships
@router.get("/", response_model=List[UserPlantResponse], tags=["User-Plants"])
def read_user_plants(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    user_plants = db.query(UserPlant).offset(skip).limit(limit).all()
    return user_plants


# READ a specific user-plant relationship by ID
@router.get("/{user_plant_id}", response_model=UserPlantResponse, tags=["User-Plants"])
def read_user_plant(user_plant_id: int, db: Session = Depends(get_db)):
    user_plant = db.query(UserPlant).filter(UserPlant.id == user_plant_id).first()
    if not user_plant:
        raise HTTPException(status_code=404, detail="User-Plant relationship not found")
    return user_plant


# UPDATE a user-plant relationship
@router.put("/{user_plant_id}", response_model=UserPlantResponse, tags=["User-Plants"])
def update_user_plant(user_plant_id: int, user_plant: UserPlantCreate, db: Session = Depends(get_db)):
    db_user_plant = db.query(UserPlant).filter(UserPlant.id == user_plant_id).first()
    if not db_user_plant:
        raise HTTPException(status_code=404, detail="User-Plant relationship not found")

    db_user_plant.image = user_plant.image
    db_user_plant.date = user_plant.date or datetime.utcnow()
    db_user_plant.description = user_plant.description
    db.commit()
    db.refresh(db_user_plant)

    return db_user_plant


# DELETE a user-plant relationship
@router.delete("/{user_plant_id}", tags=["User-Plants"])
def delete_user_plant(user_plant_id: int, db: Session = Depends(get_db)):
    user_plant = db.query(UserPlant).filter(UserPlant.id == user_plant_id).first()
    if not user_plant:
        raise HTTPException(status_code=404, detail="User-Plant relationship not found")

    db.delete(user_plant)
    db.commit()

    return {"detail": "User-Plant relationship deleted successfully"}
