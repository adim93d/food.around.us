# main.py
from fastapi import FastAPI
from dotenv import load_dotenv

from app.database.database import engine
from app.database.database import Base
from app.api.routers import plant_routes, user_routes, auth

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
    },
    {
        "name": "Auth",
        "description": "Auth related Operations"
    }
]

app = FastAPI(openapi_tags=tags_metadata)


@app.get("/")
def healthcheck():
    return f"FastAPI is up and running"

# API routes
app.include_router(plant_routes.router, prefix="/plants", tags=["Plants"])
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])