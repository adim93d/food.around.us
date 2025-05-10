# app/api/routers/plant_routes.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from dotenv import load_dotenv

from app.database.models import Plant
from app.database.database import SessionLocal
from app.database.schemas import PlantCreate, PlantResponse
from app.api.routers.auth import get_current_user

load_dotenv()

router = APIRouter(dependencies=[Depends(get_current_user)])

def get_db():
    print("Debug: Getting DB")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE plant manually
@router.post("/", response_model=PlantResponse, tags=["Plants"])
def create_plant(plant: PlantCreate, db: Session = Depends(get_db)):
    print("Debug: Creating plant")
    db_plant = db.query(Plant).filter(Plant.scientific_name == plant.scientific_name).first()
    if db_plant:
        raise HTTPException(status_code=400, detail="Plant already registered")
    new_plant = Plant(
        scientific_name=plant.scientific_name,
        family=plant.family,
        is_edible=plant.is_edible,
        edible_parts=",".join(plant.edible_parts) if plant.edible_parts else None,
        safety=plant.safety
    )
    db.add(new_plant)
    db.commit()
    db.refresh(new_plant)
    if new_plant.edible_parts:
        new_plant.edible_parts = new_plant.edible_parts.split(",")
    return new_plant

# READ all plants
@router.get("/", response_model=List[PlantResponse], tags=["Plants"])
def read_plants(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    print("Debug: Reading plants")
    plants = db.query(Plant).offset(skip).limit(limit).all()
    for plant in plants:
        plant.edible_parts = plant.edible_parts.split(",") if plant.edible_parts else []
    return plants

# READ a single plant by ID
@router.get("/{plant_id}", response_model=PlantResponse, tags=["Plants"])
def read_plant(plant_id: int, db: Session = Depends(get_db)):
    print("Debug: Reading plants by id")
    plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    plant.edible_parts = plant.edible_parts.split(",") if plant.edible_parts else []
    return plant

# UPDATE plant
@router.put("/{plant_id}", response_model=PlantResponse, tags=["Plants"])
def update_plant(plant_id: int, plant: PlantCreate, db: Session = Depends(get_db)):
    print("Debug: Updating plant")
    db_plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if not db_plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    db_plant.scientific_name = plant.scientific_name
    db_plant.family = plant.family
    db_plant.is_edible = plant.is_edible
    db_plant.edible_parts = ",".join(plant.edible_parts) if plant.edible_parts else None
    db_plant.safety = plant.safety
    db.commit()
    db.refresh(db_plant)
    db_plant.edible_parts = db_plant.edible_parts.split(",") if db_plant.edible_parts else []
    return db_plant

# DELETE plant
@router.delete("/{plant_id}", tags=["Plants"])
def delete_plant(plant_id: int, db: Session = Depends(get_db)):
    print("Debug: Deleting plant")
    plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    db.delete(plant)
    db.commit()
    return {"detail": "Plant deleted successfully"}
