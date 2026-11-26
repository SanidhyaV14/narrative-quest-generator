import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.user import User
from backend.models.project import Project
from backend.models.project_image import ProjectImage
from backend.models.generation_history import GenerationHistory
from backend.schemas.project import ImageAnalysisResponse, ImageGenerateRequest, ImageGenerateResponse
from backend.utils.security import get_current_user
from backend.utils.validators import validate_image_file
from backend.utils.file_handler import save_reference_image, image_to_base64
from backend.ai.nemotron_client import nemotron_client
from backend.ai.flux_client import flux_client

logger = logging.getLogger("routes.images")
router = APIRouter(prefix="/images", tags=["Images"])


@router.post("/analyze", response_model=ImageAnalysisResponse)
async def analyze_image(
    file: UploadFile = File(...),
    question: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Uploads and analyzes an image using NVIDIA Nemotron vision-language capabilities.
    Validates file format and size (max 5 MB).
    """
    contents = await file.read()
    fmt = validate_image_file(contents, file.filename or "image.png")
    
    # Save file to uploads/references/
    saved_path = save_reference_image(contents, file.filename or "image.png")

    # Convert to base64 for API call
    b64_str = image_to_base64(saved_path)
    mime_type = "image/png" if fmt == "PNG" else "image/jpeg"

    # Call Nemotron vision
    result = await nemotron_client.analyze_image_with_vision(
        base64_image=b64_str,
        user_question=question,
        image_mime=mime_type
    )

    data = result["data"]

    # Record history
    history = GenerationHistory(
        operation_type="IMAGE_ANALYSIS",
        model_name=result["model_used"],
        input_prompt=f"Analyzed {saved_path} with question: {question or 'N/A'}"
    )
    db.add(history)
    db.commit()

    return ImageAnalysisResponse(
        success=True,
        image_path=saved_path,
        file_path=saved_path,
        description=data.get("description", "No description generated."),
        visible_characters=data.get("visible_characters", "None identified."),
        objects=data.get("objects", "None identified."),
        environment=data.get("environment", "Not specified."),
        colors_and_atmosphere=data.get("colors_and_atmosphere", "Not specified."),
        possible_themes=data.get("possible_themes", "Creative exploration."),
        story_ideas=data.get("story_ideas", "No specific ideas."),
        model_used=result["model_used"]
    )


@router.post("/generate", response_model=ImageGenerateResponse)
async def generate_image(
    request: ImageGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generates an illustration using the NVIDIA FLUX endpoint.
    Saves image locally under uploads/generated/ and returns relative path.
    """
    result = await flux_client.generate_image(
        prompt=request.prompt,
        art_style=request.art_style,
        mood=request.mood,
        character_details=request.character_details,
        environment_details=request.environment_details,
        aspect_ratio=request.aspect_ratio
    )

    # If project_id is provided, associate image with project
    if request.project_id:
        project = db.query(Project).filter(Project.id == request.project_id).first()
        if project and project.user_id == current_user.id:
            img_record = ProjectImage(
                project_id=project.id,
                image_type="GENERATED",
                file_path=result["image_path"],
                image_prompt=result["prompt_used"]
            )
            db.add(img_record)

    # Record history
    history = GenerationHistory(
        project_id=request.project_id,
        operation_type="IMAGE_GENERATION",
        model_name=result["model_used"],
        input_prompt=result["prompt_used"]
    )
    db.add(history)
    db.commit()

    return ImageGenerateResponse(
        success=True,
        image_path=result["image_path"],
        file_path=result["image_path"],
        prompt_used=result["prompt_used"],
        model_used=result["model_used"]
    )
