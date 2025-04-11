# app/database/operations.py
from typing import Optional, List
from sqlalchemy.orm import Session
from app.database.models import Plant

def get_plant_by_scientific_name(db: Session, scientific_name: str):
    return db.query(Plant).filter(Plant.scientific_name == scientific_name).first()

def add_plant(
    db: Session,
    scientific_name: str,
    family: str,
    is_edible: bool,
    edible_parts: Optional[List[str]] = None,
    safety: Optional[str] = None
) -> Plant:
    # Convert the list of edible_parts into a comma-separated string for storage, if provided.
    edible_parts_str = ",".join(edible_parts) if edible_parts else None
    new_plant = Plant(
        scientific_name=scientific_name,
        family=family,
        is_edible=is_edible,
        edible_parts=edible_parts_str,
        safety=safety
    )
    db.add(new_plant)
    db.commit()
    db.refresh(new_plant)
    return new_plant
