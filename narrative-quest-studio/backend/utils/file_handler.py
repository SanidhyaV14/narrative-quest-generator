import os
import uuid
import base64
from pathlib import Path
from PIL import Image
import io
from fastapi import HTTPException
from backend.config import settings


def sanitize_filename(filename: str) -> str:
    """Strips path traversal elements and returns a safe base filename."""
    base = os.path.basename(filename)
    return "".join(c for c in base if c.isalnum() or c in (".", "_", "-"))


def save_reference_image(file_bytes: bytes, original_filename: str) -> str:
    """
    Saves an uploaded reference image to uploads/references/ with a unique filename.
    Returns the relative path from project root (e.g. 'uploads/references/uuid.png').
    """
    ext = original_filename.rsplit(".", 1)[-1].lower() if "." in original_filename else "png"
    unique_filename = f"ref_{uuid.uuid4().hex}.{ext}"
    dest_path = os.path.join(settings.UPLOAD_REFERENCES_DIR, unique_filename)

    with open(dest_path, "wb") as f:
        f.write(file_bytes)

    # Normalize relative path with forward slashes for portability
    return dest_path.replace("\\", "/")


def save_generated_image(image_bytes: bytes, format: str = "PNG") -> str:
    """
    Saves a generated illustration to uploads/generated/ with a unique filename.
    Returns the relative path from project root.
    """
    ext = format.lower()
    unique_filename = f"gen_{uuid.uuid4().hex}.{ext}"
    dest_path = os.path.join(settings.UPLOAD_GENERATED_DIR, unique_filename)

    with open(dest_path, "wb") as f:
        f.write(image_bytes)

    return dest_path.replace("\\", "/")


def image_to_base64(file_path: str) -> str:
    """Reads an image from disk and converts it to a base64 string."""
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Image file not found at {file_path}")
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def delete_project_images(image_paths: list[str]) -> None:
    """Safely deletes image files from disk when a project is removed."""
    for path_str in image_paths:
        try:
            p = Path(path_str)
            # Ensure path is within uploads directory to prevent accidental file deletion
            if p.is_file() and any(upload_dir in str(p.resolve()) for upload_dir in ("references", "generated")):
                p.unlink(missing_ok=True)
        except Exception:
            pass
