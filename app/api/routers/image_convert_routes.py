# app/api/routers/image_convert_routes.py

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import List
from io import BytesIO
from PIL import Image
from app.api.routers.auth import get_current_user

router = APIRouter(dependencies=[Depends(get_current_user)])

async def convert_images_for_plantnet(images: List[UploadFile]) -> List[UploadFile]:
    """
    Convert uploaded images to JPEG RGB format as required by the PlantNet API.
    Returns a list of UploadFile instances containing JPEG data.
    """
    converted_images: List[UploadFile] = []

    for image in images:
        contents = await image.read()
        try:
            img = Image.open(BytesIO(contents))
            if img.mode != "RGB":
                img = img.convert("RGB")

            buf = BytesIO()
            img.save(buf, format="JPEG")
            buf.seek(0)

            new_filename = f"{image.filename.rsplit('.', 1)[0]}.jpg"
            new_file = BytesIO(buf.getvalue())

            # Instantiate without unsupported keyword, then set content_type
            converted = UploadFile(new_filename, new_file)
            converted.content_type = "image/jpeg"

            converted_images.append(converted)

        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to convert image {image.filename}: {e}"
            )

    return converted_images

@router.post("/", summary="Convert images for PlantNet API")
async def convert_route(
    images: List[UploadFile] = File(...)
):
    """
    Endpoint to convert one or more images into PlantNet-compatible JPEGs.
    """
    converted = await convert_images_for_plantnet(images)
    return {"converted_filenames": [img.filename for img in converted]}
