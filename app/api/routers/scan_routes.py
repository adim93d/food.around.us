from app.services.ai_service import get_detailed_plant_info
from app.api.routers.identify_routes import identify_plant  # Import the async function
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.concurrency import run_in_threadpool  # Import run_in_threadpool to run sync functions in a thread pool
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
    family_name = plant_info.get("family_name")
    if not scientific_name:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve scientific name from identification result."
        )

    # Use run_in_threadpool to call the synchronous function in a non-blocking way.
    ai_response = await run_in_threadpool(get_detailed_plant_info, scientific_name)
    is_edible = ai_response.get("edible")
    edible_parts = ai_response.get("edible_parts")
    safety = ai_response.get("safety")

    return {
        "Scientific name: ": scientific_name,
        "Family name: ": family_name,
        "Edible: ": is_edible,
        "Edible parts: ": edible_parts,
        "Safety: ": safety
    }
