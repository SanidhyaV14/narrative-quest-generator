from typing import Optional, List, Any, Dict
from pydantic import BaseModel, Field
from datetime import datetime


class ProjectCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    project_type: str = Field(..., description="'STORY' or 'GAME_QUEST'")
    input_data: Dict[str, Any]
    generated_content: Dict[str, Any]
    image_paths: Optional[List[str]] = Field(default_factory=list)
    image_prompt: Optional[str] = None
    image_description: Optional[str] = None


class ProjectImageResponse(BaseModel):
    id: int
    image_type: str
    file_path: str
    image_prompt: Optional[str] = None
    image_description: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ProjectResponse(BaseModel):
    id: int
    user_id: int
    title: str
    project_type: str
    input_data: Dict[str, Any]
    generated_content: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    images: List[ProjectImageResponse] = []

    class Config:
        from_attributes = True


class ProjectListResponse(BaseModel):
    projects: List[ProjectResponse]
    total: int


class FeedbackCreateRequest(BaseModel):
    project_id: int
    rating: int = Field(..., ge=1, le=5)
    comments: Optional[str] = None


class FeedbackResponse(BaseModel):
    id: int
    project_id: int
    user_id: int
    rating: int
    comments: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class ImageAnalysisResponse(BaseModel):
    success: bool
    image_path: str
    file_path: Optional[str] = None
    description: str
    visible_characters: str
    objects: str
    environment: str
    colors_and_atmosphere: str
    possible_themes: str
    story_ideas: str
    model_used: str


class ImageGenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=3, description="Illustration description")
    art_style: str = Field("Fantasy illustration", description="Art style")
    mood: str = Field("Dramatic", description="Mood")
    character_details: Optional[str] = None
    environment_details: Optional[str] = None
    aspect_ratio: Optional[str] = None
    project_id: Optional[int] = None


class ImageGenerateResponse(BaseModel):
    success: bool
    image_path: str
    file_path: Optional[str] = None
    prompt_used: str
    model_used: str
