from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from typing import List, Annotated
import requests
import os
from dotenv import load_dotenv
from io import BytesIO
from app.api.routers.auth import get_current_user
from app.services.ai_service import get_detailed_plant_info

load_dotenv()

router = APIRouter(dependencies=[Depends(get_current_user)])
API_KEY = os.getenv("PLANETNET_API_KEY")
PROJECT = "all"
API_ENDPOINT = f"https://my-api.plantnet.org/v2/identify/{PROJECT}?api-key={API_KEY}"


@router.post("/", tags=["Identify"])
async def identify_plant(
        organs: Annotated[List[str], Form(...)],
        images: Annotated[List[UploadFile], File(...)]
):
    if not images:
        raise HTTPException(status_code=400, detail="No images provided")

    files = []
    for image in images:
        # Validate that the file type is acceptable per the PlantNet API docs.
        if image.content_type not in ("image/jpeg", "image/png"):
            raise HTTPException(status_code=400, detail="Unsupported file type. Only JPEG and PNG are allowed.")

        # Read the file contents
        contents = await image.read()

        # (Optional) Check file size here if the API restricts the size, e.g.:
        # if len(contents) > MAX_FILE_SIZE:
        #     raise HTTPException(status_code=400, detail="File size exceeds allowed limit.")

        # Wrap the bytes in a BytesIO object so requests can correctly encode it
        files.append(('images', (image.filename, BytesIO(contents), image.content_type)))

    data = [('organs', organ) for organ in organs]

    try:
        response = requests.post(API_ENDPOINT, files=files, data=data)
        if response.status_code != 200:
            error_detail = f"PlantNet API error {response.status_code}: {response.text}"
            raise HTTPException(status_code=response.status_code, detail=error_detail)

        result = response.json()
        if not result.get('results'):
            raise HTTPException(status_code=404, detail="No identification results found.")

        top_result = result['results'][0]
        species_name = top_result['species']['scientificNameWithoutAuthor']
        family_name = top_result['species']['family']['scientificNameWithoutAuthor']
        #
        # plant_info = get_detailed_plant_info(species_name)
        # is_edible = plant_info.get("edible")
        # edible_parts = plant_info.get("edible_parts")
        # safety = plant_info.get("safety")

        return {
            "species_name": species_name,
            "family_name": family_name,
            # "is_edible": is_edible,
            # "edible_parts": edible_parts,
            # "safety": safety
        }

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Request error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
