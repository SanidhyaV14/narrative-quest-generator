from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query, Response
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.user import User
from backend.models.project import Project
from backend.models.project_image import ProjectImage
from backend.schemas.project import (
    ProjectCreateRequest,
    ProjectResponse,
    ProjectListResponse,
    ProjectImageResponse
)
from backend.utils.security import get_current_user
from backend.utils.file_handler import delete_project_images

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    request: ProjectCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Saves a new Story or Game Quest project."""
    if request.project_type not in ("STORY", "GAME_QUEST"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="project_type must be either 'STORY' or 'GAME_QUEST'."
        )

    # Create project record
    project = Project(
        user_id=current_user.id,
        title=request.title.strip(),
        project_type=request.project_type,
        input_data=request.input_data,
        generated_content=request.generated_content
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    # Attach any associated image paths
    if request.image_paths:
        for p in request.image_paths:
            img_type = "UPLOAD" if "references" in p else "GENERATED"
            img_record = ProjectImage(
                project_id=project.id,
                image_type=img_type,
                file_path=p,
                image_prompt=request.image_prompt,
                image_description=request.image_description
            )
            db.add(img_record)
        db.commit()
        db.refresh(project)

    return ProjectResponse.model_validate(project)


@router.get("", response_model=ProjectListResponse)
def list_projects(
    project_type: Optional[str] = Query(None, description="Filter by STORY or GAME_QUEST"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieves all projects owned by the authenticated user."""
    query = db.query(Project).filter(Project.user_id == current_user.id)
    if project_type:
        query = query.filter(Project.project_type == project_type.upper())
    
    projects = query.order_by(Project.created_at.desc()).all()
    return ProjectListResponse(
        projects=[ProjectResponse.model_validate(p) for p in projects],
        total=len(projects)
    )


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project_details(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieves full details of a specific project. Only the project owner can access."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")
    
    if project.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: You do not have permission to view this project."
        )

    return ProjectResponse.model_validate(project)


@router.delete("/{project_id}", status_code=status.HTTP_200_OK)
def delete_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Deletes a project and its associated local images."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")
    
    if project.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: You do not have permission to delete this project."
        )

    # Collect image file paths to clean up from disk
    image_paths = [img.file_path for img in project.images]
    delete_project_images(image_paths)

    db.delete(project)
    db.commit()
    return {"message": "Project and associated images deleted successfully.", "id": project_id}


@router.get("/{project_id}/export")
def export_project_as_txt(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Exports a project formatted as a clean plain text document."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")
    
    if project.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: You do not have permission to export this project."
        )

    # Format document
    content = project.generated_content or {}
    inputs = project.input_data or {}
    
    lines = [
        "=" * 70,
        f"NARRATIVE STUDIO - PROJECT EXPORT",
        f"Title: {project.title}",
        f"Project Type: {project.project_type}",
        f"Created Date: {project.created_at.strftime('%Y-%m-%d %H:%M:%S UTC')}",
        "=" * 70,
        "",
        "--- USER INPUTS ---"
    ]
    for k, v in inputs.items():
        lines.append(f"{k.replace('_', ' ').capitalize()}: {v}")

    lines.append("")
    lines.append("--- GENERATED CONTENT ---")

    if project.project_type == "STORY":
        lines.extend([
            f"Title: {content.get('title', project.title)}",
            f"Genre: {content.get('genre', '')}",
            "",
            "INTRODUCTION:",
            content.get("introduction", ""),
            "",
            "MAIN CHARACTERS:",
            content.get("main_characters", ""),
            "",
            "SETTING:",
            content.get("setting", ""),
            "",
            "MAIN CONFLICT:",
            content.get("conflict", ""),
            "",
            "COMPLETE STORY:",
            content.get("complete_story", ""),
            "",
            "ENDING:",
            content.get("ending", ""),
            "",
            "SUGGESTED IMAGE DESCRIPTION:",
            content.get("suggested_image_description", "")
        ])
    else:  # GAME_QUEST
        lines.extend([
            f"Quest Title: {content.get('title', project.title)}",
            f"Description: {content.get('quest_description', '')}",
            "",
            "BACKGROUND STORY:",
            content.get("background_story", ""),
            "",
            "MAIN CHARACTER:",
            content.get("main_character", ""),
            "",
            "NPCS & ROLES:",
            content.get("npcs", ""),
            "",
            "OBJECTIVES:",
            content.get("objectives", ""),
            "",
            "CHALLENGES & OBSTACLES:",
            content.get("challenges", ""),
            "",
            "EXAMPLE DIALOGUE:",
            content.get("dialogue", ""),
            "",
            "REWARDS:",
            content.get("rewards", ""),
            "",
            "ENDING:",
            content.get("ending", ""),
            "",
            "SUGGESTED ILLUSTRATION DESCRIPTION:",
            content.get("suggested_illustration_description", "")
        ])

    if project.images:
        lines.append("")
        lines.append("--- ASSOCIATED IMAGES ---")
        for img in project.images:
            lines.append(f"- [{img.image_type}] {img.file_path}")
            if img.image_prompt:
                lines.append(f"  Prompt: {img.image_prompt}")

    lines.append("")
    lines.append("=" * 70)
    lines.append("Exported from Narrative Studio")

    text_body = "\n".join(lines)
    filename = f"{project.title.lower().replace(' ', '_')}_{project.id}.txt"

    return Response(
        content=text_body,
        media_type="text/plain; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )
