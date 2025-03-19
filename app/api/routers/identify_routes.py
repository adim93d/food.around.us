from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from typing import List
import requests
import os
from dotenv import load_dotenv
from app.api.routers.auth import get_current_user

load_dotenv()

router = APIRouter(dependencies=[Depends(get_current_user)])

API_KEY = os.getenv("PLANETNET_API_KEY")  # Add this in your .env file
PROJECT = "all"
API_ENDPOINT = f"https://my-api.plantnet.org/v2/identify/{PROJECT}?api-key={API_KEY}"


@router.post("/", tags=["Identify"])
async def identify_plant(
    organs: List[str] = Form(...),
    images: List[UploadFile] = File(...)
):
    if not images:
        raise HTTPException(status_code=400, detail="No images provided")

    files = []
    for image in images:
        contents = await image.read()
        files.append(('images', (image.filename, contents, image.content_type)))

    data = {'organs': organs}

    try:
        response = requests.post(API_ENDPOINT, files=files, data=data)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to identify plant")

        result = response.json()
        if not result.get('results'):
            raise ValueError("No identification results found.")

        top_result = result['results'][0]
        species_name = top_result['species']['scientificNameWithoutAuthor']
        family_name = top_result['species']['family']['scientificNameWithoutAuthor']

        return species_name, family_name

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
