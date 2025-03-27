from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from typing import List
import requests
import os
from dotenv import load_dotenv
from app.api.routers.auth import get_current_user
from app.services.ai_service import get_detailed_plant_info

load_dotenv()

router = APIRouter(dependencies=[Depends(get_current_user)])
API_KEY = os.getenv("PLANETNET_API_KEY")
PROJECT = "all"
API_ENDPOINT = f"https://my-api.plantnet.org/v2/identify/{PROJECT}?api-key={API_KEY}"


@router.post("/", tags=["Identify"])
async def identify_plant(
        organs: List[str] = Form(...),
        images: List[UploadFile] = File(...)):
    if not images:
        raise HTTPException(status_code=400, detail="No images provided")

    files = []
    for image in images:
        contents = await image.read()
        print(contents)
        print(image.filename)
        print(image.content_type)
        files.append(('images', (image.filename, contents, image.content_type)))

    data = [('organs', organ) for organ in organs]

    try:
        print("Starting first API call to Planetnet")
        response = requests.post(API_ENDPOINT, files=files, data=data)

        if response.status_code != 200:
            # Log PlantNet error
            error_detail = f"PlantNet API error {response.status_code}: {response.text}"
            raise HTTPException(status_code=response.status_code, detail=error_detail)

        result = response.json()
        print(f"Finished first API Call: {result}")
        print(result)
        if not result.get('results'):
            raise HTTPException(status_code=404, detail="No identification results found.")

        top_result = result['results'][0]
        species_name = top_result['species']['scientificNameWithoutAuthor']
        family_name = top_result['species']['family']['scientificNameWithoutAuthor']
        print("Starting 2 API code to OpenAI")
        plant_info = get_detailed_plant_info(species_name)
        is_edible = plant_info.get("edible")
        edible_parts = plant_info.get("edible_parts")
        safety = plant_info.get("safety")
        print(f"Finsished 2 API call: result: {plant_info}")

        return {"species_name": species_name, "family_name": family_name, "is_edible": is_edible, "edible_parts": edible_parts, "safety": safety}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Request error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
