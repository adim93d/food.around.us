
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.concurrency import run_in_threadpool
from typing import List, Annotated
from sqlalchemy.orm import Session

from app.api.routers.auth import get_current_user
from app.api.routers.image_convert_routes import convert_images_for_plantnet
from app.api.routers.identify_routes import identify_plant
from app.database.database import SessionLocal
from app.database.operations import get_plant_by_scientific_name, add_plant
from app.services.ai_service import get_detailed_plant_info
from app.database.models import UserPlant

router = APIRouter(dependencies=[Depends(get_current_user)])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", tags=["Scan"], summary="Scan images, identify plant, enrich and save")
async def scan_and_chain(
    organs: Annotated[List[str], Form(...)],
    images: Annotated[List[UploadFile], File(...)],
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    print("Debug: Scan and chain")
    # Step 0: Convert images into PlantNet-compatible JPEGs
    converted_images = await convert_images_for_plantnet(images)

    # Step 1: Identify the plant using the PlantNet API.
    plant_info = await identify_plant(organs, converted_images)
    print(f"Plant info: {plant_info}")
    scientific_name = plant_info.get("species_name")
    family_name = plant_info.get("family_name")
    common_names = plant_info.get("common_names")
    if not scientific_name:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve scientific name from identification result."
        )

    # Step 2: Look up the plant in the database.
    plant = get_plant_by_scientific_name(db, scientific_name)
    if plant:
        edible_parts_list = plant.edible_parts.split(",") if plant.edible_parts else []
    else:
        # Step 3: Get detailed plant info via OpenAI
        ai_response = await run_in_threadpool(get_detailed_plant_info, scientific_name)
        print(f"Debug - Ai response: {ai_response}")
        is_edible = ai_response.get("edible")
        edible_parts = ai_response.get("edible_parts")  # May be None
        edible_parts_list = edible_parts.split(",") if edible_parts else []

        # Step 4: Save the new plant in the database.
        print(f"Debug: Creating plant")
        plant = add_plant(
            db,
            scientific_name,
            family_name,
            common_names,
            is_edible,
            edible_parts
        )
        print(f"Debug: plant created = {plant}")

    # Step 5: Associate the plant with the current user.
    print(f"Debug: Link plant to user")
    user_plant = UserPlant(user_id=current_user.id, plant_id=plant.id)
    print(f"Debug: link = {user_plant}")
    print(f"Debug: Adding to db")
    db.add(user_plant)
    db.commit()
    print(f"Debug: Added to db")

    # Step 6: Build and return the response.
    response_data = {
        "plant": {
            "Scientific name: ": plant.scientific_name,
            "Family name: ": plant.family,
            "Common names: ": common_names,
            "Edible: ": plant.is_edible,
            "Edible parts: ": edible_parts_list,
            "Safety: ": plant.safety,
            "Created at: ": plant.created_at.isoformat()
        }
    }
    print(f"Debug: DB response = {response_data}")
    return response_data
