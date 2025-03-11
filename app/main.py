# main.py
from fastapi import FastAPI, HTTPException, Depends

from dotenv import load_dotenv
from app.database.database import SessionLocal, engine
from app.database.database import Base
from app.api.routers import plant_routes, user_routes

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

app = FastAPI(openapi_tags=tags_metadata)

app.include_router(plant_routes.router, prefix="/plants", tags=["Plants"])
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
