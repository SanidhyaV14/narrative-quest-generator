import re
from fastapi import HTTPException, UploadFile, status
from PIL import Image
import io
from backend.config import settings

EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/jpg"}


def validate_email(email: str) -> bool:
    """Validates email format using regex."""
    if not email or not re.match(EMAIL_REGEX, email.strip()):
        return False
    return True


def validate_image_file(file_bytes: bytes, filename: str) -> str:
    """
    Validates uploaded image file:
    - Maximum size: MAX_UPLOAD_SIZE_MB
    - Allowed extensions: jpg, jpeg, png
    - Validates actual image binary using Pillow
    Returns image format (e.g. 'JPEG' or 'PNG').
    """
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if len(file_bytes) > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Image size exceeds the maximum allowed limit of {settings.MAX_UPLOAD_SIZE_MB} MB."
        )

    # Extension check
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file extension '.{ext}'. Allowed types are JPG, JPEG, and PNG."
        )

    # Pillow format check
    try:
        with Image.open(io.BytesIO(file_bytes)) as img:
            img.verify()
            fmt = img.format
            if fmt not in ("JPEG", "PNG"):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid image format '{fmt}'. Only JPG/PNG images are supported."
                )
            return fmt
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is corrupted or not a valid image."
        )
