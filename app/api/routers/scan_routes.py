from app.services.ai_service import get_detailed_plant_info
from app.api.routers.identify_routes import identify_plant  # Import the async function
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from typing import List, Annotated
from app.api.routers.auth import get_current_user

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post("/", tags=["Scan"])
async def scan_and_ai(
        organs: Annotated[List[str], Form(...)],
        images: Annotated[List[UploadFile], File(...)]
):
    plant_info = await identify_plant(organs, images)
    scientific_name = plant_info.get("species_name")
    if not scientific_name:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve scientific name from identification result."
        )

    ai_response = get_detailed_plant_info(scientific_name)

    return ai_response
