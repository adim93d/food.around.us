from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from dotenv import load_dotenv

from app.database.models import Recipe
from app.database.database import Base, SessionLocal, engine
from app.database.schemas import RecipeCreate, RecipeResponse
from app.api.routers.auth import get_current_user

load_dotenv()

# All endpoints in this router require authentication
router = APIRouter(dependencies=[Depends(get_current_user)])


# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create recipe
@router.post("/", response_model=RecipeResponse, tags=["Recipes"])
def create_recipe(recipe: RecipeCreate, db: Session = Depends(get_db)):
    db_recipe = db.query(Recipe).filter(Recipe.name == recipe.name).first()
    if db_recipe:
        raise HTTPException(status_code=400, detail="Plant already registered")
    new_recipe = Recipe(name=recipe.name, content=recipe.content)
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    return new_recipe


# READ all recipes
@router.get("/", response_model=List[RecipeResponse], tags=["Recipes"])
def read_recipes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    recipes = db.query(Recipe).offset(skip).limit(limit).all()
    return recipes


# READ a single recipe by ID
@router.get("/{recipe_id}", response_model=RecipeResponse, tags=["Recipes"])
def read_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


# UPDATE recipe
@router.put("/{recipe_id}", response_model=RecipeResponse, tags=["Recipes"])
def update_recipe(recipe_id: int, recipe: RecipeCreate, db: Session = Depends(get_db)):
    db_recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    db_recipe.name = recipe.name
    db_recipe.content = recipe.content
    db.commit()
    db.refresh(db_recipe)
    return db_recipe


# DELETE recipe
@router.delete("/{recipe_id}", tags=["Recipes"])
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    db.delete(recipe)
    db.commit()
    return {"detail": "Recipe deleted successfully"}
