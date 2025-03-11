from fastapi import APIRouter, FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from dotenv import load_dotenv
from app.database.models import Plant
from app.database.database import Base
from app.database.database import SessionLocal, engine
from app.database.schemas import PlantCreate, PlantResponse

load_dotenv()

# Create tables if they do not exist
Base.metadata.create_all(bind=engine)

tags_metadata = [
    {
        "name": "Users",
        "description": "CRUD Operations related to users."
    },
    {
        "name": "Plants",
        "description": "CRUD Operations related to plants."
    }
]
router = APIRouter()
app = FastAPI(openapi_tags=tags_metadata)

# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create plant
@router.post("/", response_model=PlantResponse, tags=["Plants"])
def create_plant(plant: PlantCreate, db: Session = Depends(get_db)):
    db_plant = db.query(Plant).filter(Plant.scientific_name == plant.scientific_name).first()
    if db_plant:
        raise HTTPException(status_code=400, detail="Plant already registered")
    new_plant = Plant(scientific_name=plant.scientific_name, family=plant.family, is_edible=plant.is_edible)
    db.add(new_plant)
    db.commit()
    db.refresh(new_plant)
    return new_plant

# READ all plants
@router.get("/", response_model=List[PlantResponse], tags=["Plants"])
def read_plants(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    plants = db.query(Plant).offset(skip).limit(limit).all()
    return plants

# READ a single plant by ID
@router.get("/{plant_id}", response_model=PlantResponse, tags=["Plants"])
def read_plant(plant_id: int, db: Session = Depends(get_db)):
    plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant

# UPDATE plant
@router.put("/{plant_id}", response_model=PlantResponse, tags=["Plants"])
def update_plant(plant_id: int, plant: PlantCreate, db: Session = Depends(get_db)):
    db_plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if not db_plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    db_plant.scientific_name = plant.scientific_name
    db_plant.family = plant.family
    db_plant.is_edible = plant.is_edible
    db.commit()
    db.refresh(db_plant)
    return db_plant

# DELETE user
@router.delete("/{plant_id}", tags=["Plants"])
def delete_plant(plant_id: int, db: Session = Depends(get_db)):
    plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    db.delete(plant)
    db.commit()
    return {"detail": "Plant deleted successfully"}
