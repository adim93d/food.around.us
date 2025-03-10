# main.py
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from dotenv import load_dotenv
from database import SessionLocal, engine
import models, schemas

load_dotenv()

# Create tables if they do not exist
models.Base.metadata.create_all(bind=engine)

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

app = FastAPI(openapi_tags=tags_metadata)

# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE user
@app.post("/users/", response_model=schemas.UserResponse, tags=["Users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = models.User(email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# READ all users
@app.get("/users/", response_model=List[schemas.UserResponse], tags=["Users"])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

# READ a single user by ID
@app.get("/users/{user_id}", response_model=schemas.UserResponse, tags=["Users"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# UPDATE user
@app.put("/users/{user_id}", response_model=schemas.UserResponse, tags=["Users"])
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.email = user.email
    db_user.password = user.password
    db.commit()
    db.refresh(db_user)
    return db_user

# DELETE user
@app.delete("/users/{user_id}", tags=["Users"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}

# Create plant
@app.post("/plants/", response_model=schemas.PlantResponse, tags=["Plants"])
def create_plant(plant: schemas.PlantCreate, db: Session = Depends(get_db)):
    db_plant = db.query(models.Plant).filter(models.Plant.scientific_name == plant.scientific_name).first()
    if db_plant:
        raise HTTPException(status_code=400, detail="Plant already registered")
    new_plant = models.Plant(scientific_name=plant.scientific_name, family=plant.family, is_edible=plant.is_edible)
    db.add(new_plant)
    db.commit()
    db.refresh(new_plant)
    return new_plant

# READ all plants
@app.get("/plants/", response_model=List[schemas.PlantResponse], tags=["Plants"])
def read_plants(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    plants = db.query(models.Plant).offset(skip).limit(limit).all()
    return plants

# READ a single plant by ID
@app.get("/plants/{plant_id}", response_model=schemas.PlantResponse, tags=["Plants"])
def read_plant(plant_id: int, db: Session = Depends(get_db)):
    plant = db.query(models.Plant).filter(models.Plant.id == plant_id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant

# UPDATE plant
@app.put("/plants/{plant_id}", response_model=schemas.PlantResponse, tags=["Plants"])
def update_plant(plant_id: int, plant: schemas.PlantCreate, db: Session = Depends(get_db)):
    db_plant = db.query(models.Plant).filter(models.Plant.id == plant_id).first()
    if not db_plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    db_plant.scientific_name = plant.scientific_name
    db_plant.family = plant.family
    db_plant.is_edible = plant.is_edible
    db.commit()
    db.refresh(db_plant)
    return db_plant

# DELETE user
@app.delete("/plants/{plant_id}", tags=["Plants"])
def delete_plant(plant_id: int, db: Session = Depends(get_db)):
    plant = db.query(models.Plant).filter(models.Plant.id == plant_id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    db.delete(plant)
    db.commit()
    return {"detail": "Plant deleted successfully"}
