# app/api/routers/image_convert_routes.py

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import List
from io import BytesIO
from PIL import Image
from app.api.routers.auth import get_current_user

router = APIRouter(dependencies=[Depends(get_current_user)])

class ConvertedImage:
    print("Debug: Converting image class")
    """
    A minimal stand-in for UploadFile that holds JPEG bytes,
    plus filename and content_type attributes.
    """
    def __init__(self, filename: str, data: bytes, content_type: str):
        self.filename = filename
        self.content_type = content_type
        self._data = data

    async def read(self) -> bytes:
        return self._data

    @property
    def file(self) -> BytesIO:
        return BytesIO(self._data)


async def convert_images_for_plantnet(images: List[UploadFile]) -> List[ConvertedImage]:
    """
    Convert uploaded images to JPEG/RGB format as required by PlantNet.
    Returns a list of ConvertedImage instances.
    """
    converted_images: List[ConvertedImage] = []
    print("Debug: Converting img for plantnet")

    for image in images:
        raw = await image.read()
        try:
            img = Image.open(BytesIO(raw))
            if img.mode != "RGB":
                img = img.convert("RGB")

            buf = BytesIO()
            img.save(buf, format="JPEG")
            jpeg_bytes = buf.getvalue()
            new_name = f"{image.filename.rsplit('.', 1)[0]}.jpg"

            converted_images.append(
                ConvertedImage(new_name, jpeg_bytes, "image/jpeg")
            )

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
    print("Debug: Convert route")
    """
    Endpoint to convert one or more images into PlantNet-compatible JPEGs.
    """
    out = await convert_images_for_plantnet(images)
    return {"converted_filenames": [img.filename for img in out]}
