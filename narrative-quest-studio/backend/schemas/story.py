from typing import Optional, List
from pydantic import BaseModel, Field


class StoryGenerateRequest(BaseModel):
    genre: str = Field("Fantasy", description="Genre of the story")
    theme: str = Field("Adventure", description="Theme of the story")
    setting: str = Field(..., min_length=2, description="Setting or location description")
    main_character: str = Field(..., min_length=2, description="Main character details")
    story_idea: str = Field(..., min_length=5, description="Core plot idea or premise")
    story_length: str = Field("Medium", description="Short, Medium, or Long")
    tone: str = Field("Suspenseful", description="Tone (Dark, Emotional, Humorous, Suspenseful, Inspirational)")
    additional_instructions: Optional[str] = Field(None, description="Optional extra directions")
    reference_image_path: Optional[str] = Field(None, description="Relative path of previously uploaded reference image")


class StoryStructuredContent(BaseModel):
    title: str
    genre: str
    introduction: str
    main_characters: str
    setting: str
    conflict: str
    complete_story: str
    ending: str
    suggested_image_description: str


class StoryResponse(BaseModel):
    success: bool
    data: StoryStructuredContent
    model_used: str
    prompt_tokens: Optional[int] = None
