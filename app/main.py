
from fastapi import FastAPI
from dotenv import load_dotenv
import logging
from contextlib import asynccontextmanager
import os

from app.database.database import engine, Base

from app.api.routers import (
    plant_routes,
    user_routes,
    user_plants_routes,
    recipe_routes,
    identify_routes,
    scan_routes,
    auth
)
from app.api.routers.image_convert_routes import router as image_convert_router

load_dotenv()
logging.basicConfig(level=logging.INFO)

# Create all DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def healthcheck():
    return "FastAPI is up and running!"

# API routes
app.include_router(identify_routes.router, prefix="/identify", tags=["Identify"])
app.include_router(scan_routes.router, prefix="/scan", tags=["Scan"])
app.include_router(image_convert_router, prefix="/convert", tags=["Convert"])
app.include_router(plant_routes.router, prefix="/plants", tags=["Plants"])
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(user_plants_routes.router, prefix="/user_plants", tags=["User-Plants"])
app.include_router(recipe_routes.router, prefix="/recipes", tags=["Recipes"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
