from typing import Optional, List
from pydantic import BaseModel, Field


class QuestGenerateRequest(BaseModel):
    game_genre: str = Field("RPG", description="RPG, Fantasy, Adventure, Survival, Mystery, Science Fiction")
    theme: str = Field("Treasure Hunt", description="Rescue, Treasure Hunt, Mystery, Exploration, Revenge, Survival")
    setting: str = Field(..., min_length=2, description="Game world / quest location")
    difficulty: str = Field("Medium", description="Easy, Medium, Hard")
    main_character: str = Field(..., min_length=2, description="Protagonist or player character")
    quest_objective: str = Field(..., min_length=3, description="Core quest objective")
    missions: int = Field(3, ge=1, le=10, description="Number of quest missions/stages")
    ending_preference: str = Field("Victory", description="Victory, Failure, Unexpected Twist, Open Ending")
    additional_instructions: Optional[str] = Field(None, description="Optional game design instructions")
    reference_image_path: Optional[str] = Field(None, description="Relative path to reference image")


class QuestStructuredContent(BaseModel):
    title: str
    quest_description: str
    background_story: str
    main_character: str
    npcs: str
    objectives: str
    challenges: str
    dialogue: str
    rewards: str
    ending: str
    suggested_illustration_description: str


class QuestResponse(BaseModel):
    success: bool
    data: QuestStructuredContent
    model_used: str
    prompt_tokens: Optional[int] = None
