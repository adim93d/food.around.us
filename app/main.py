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
    auth,
    recipe_routes,
    identify_routes,
    scan_routes
)
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

# WARNING: Do not drop tables in production!
if os.getenv("RUN_DB_INIT", "false").lower() == "true":
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
else:
    Base.metadata.create_all(bind=engine)

tags_metadata = [
    {"name": "Users", "description": "CRUD Operations related to users."},
    {"name": "Identify", "description": "Operations related to identifying plants."},
    {"name": "Plants", "description": "CRUD Operations related to plants."},
    {"name": "User-Plants", "description": "CRUD Operations related to User-Plants relationship."},
    {"name": "Recipes", "description": "CRUD Operations related to recipes."},
    {"name": "Auth", "description": "Auth related Operations"}
]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("FastAPI is starting up...")
    yield
    logger.info("FastAPI is shutting down...")

app = FastAPI(openapi_tags=tags_metadata, lifespan=lifespan)

# Add CORS middleware to allow requests from your v0.dev front end.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://v0-food-around-us.vercel.app",
                   "https://v0-food-around-us.vercel.app/",
                   "https://v0-food-around-us.vercel.app/scan/",
                   "https://v0-food-around-us.vercel.app/scan"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],  # Add this to expose all headers
)

@app.get("/")
def healthcheck():
    return "FastAPI is up and running!"

# API routes
app.include_router(identify_routes.router, prefix="/identify", tags=["Identify"])
app.include_router(scan_routes.router, prefix="/scan", tags=["Scan"])
app.include_router(plant_routes.router, prefix="/plants", tags=["Plants"])
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(user_plants_routes.router, prefix="/user_plants", tags=["User-Plants"])
app.include_router(recipe_routes.router, prefix="/recipes", tags=["Recipes"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
