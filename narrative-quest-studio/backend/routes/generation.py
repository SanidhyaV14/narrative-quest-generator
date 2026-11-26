import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.user import User
from backend.models.generation_history import GenerationHistory
from backend.schemas.story import StoryGenerateRequest, StoryResponse, StoryStructuredContent
from backend.schemas.quest import QuestGenerateRequest, QuestResponse, QuestStructuredContent
from backend.utils.security import get_current_user
from backend.utils.file_handler import image_to_base64
from backend.ai.nemotron_client import nemotron_client
from backend.ai.prompt_templates import (
    STORY_SYSTEM_PROMPT,
    build_story_user_prompt,
    QUEST_SYSTEM_PROMPT,
    build_quest_user_prompt
)

logger = logging.getLogger("routes.generation")
router = APIRouter(prefix="/generate", tags=["Generation"])


@router.post("/story", response_model=StoryResponse)
async def generate_story(
    request: StoryGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generates a structured narrative story using NVIDIA Nemotron.
    If a reference image path is provided, vision analysis is used as context.
    """
    image_context = ""
    if request.reference_image_path:
        try:
            b64_img = image_to_base64(request.reference_image_path)
            analysis = await nemotron_client.analyze_image_with_vision(b64_img)
            vis_data = analysis.get("data", {})
            image_context = (
                f"Visual details from uploaded image: Setting={vis_data.get('environment', '')}, "
                f"Characters={vis_data.get('visible_characters', '')}, Atmosphere={vis_data.get('colors_and_atmosphere', '')}"
            )
        except Exception as e:
            logger.warning(f"Could not analyze reference image for story: {e}")

    # Build prompt
    user_prompt = build_story_user_prompt(
        genre=request.genre,
        theme=request.theme,
        setting=request.setting,
        main_character=request.main_character,
        story_idea=request.story_idea,
        story_length=request.story_length,
        tone=request.tone,
        additional_instructions=request.additional_instructions or "",
        image_context=image_context
    )

    # Call AI client
    result = await nemotron_client.generate_chat_completion(
        system_prompt=STORY_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        temperature=0.75
    )

    raw_data = result["data"]
    try:
        structured_story = StoryStructuredContent(
            title=raw_data.get("title", "Untitled Story"),
            genre=raw_data.get("genre", request.genre),
            introduction=raw_data.get("introduction", ""),
            main_characters=raw_data.get("main_characters", request.main_character),
            setting=raw_data.get("setting", request.setting),
            conflict=raw_data.get("conflict", ""),
            complete_story=raw_data.get("complete_story", ""),
            ending=raw_data.get("ending", ""),
            suggested_image_description=raw_data.get("suggested_image_description", "")
        )
    except Exception as e:
        logger.error(f"Failed to validate story structure: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"AI model output could not be formatted into structured story: {str(e)}"
        )

    # Record history
    history = GenerationHistory(
        operation_type="STORY",
        model_name=result["model_used"],
        input_prompt=user_prompt[:2000]
    )
    db.add(history)
    db.commit()

    return StoryResponse(
        success=True,
        data=structured_story,
        model_used=result["model_used"],
        prompt_tokens=result.get("prompt_tokens")
    )


@router.post("/quest", response_model=QuestResponse)
async def generate_quest(
    request: QuestGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generates a structured video-game quest using NVIDIA Nemotron.
    """
    image_context = ""
    if request.reference_image_path:
        try:
            b64_img = image_to_base64(request.reference_image_path)
            analysis = await nemotron_client.analyze_image_with_vision(b64_img)
            vis_data = analysis.get("data", {})
            image_context = (
                f"Visual reference: Environment={vis_data.get('environment', '')}, "
                f"Entities={vis_data.get('visible_characters', '')}, Atmosphere={vis_data.get('colors_and_atmosphere', '')}"
            )
        except Exception as e:
            logger.warning(f"Could not analyze reference image for quest: {e}")

    # Build prompt
    user_prompt = build_quest_user_prompt(
        game_genre=request.game_genre,
        theme=request.theme,
        setting=request.setting,
        difficulty=request.difficulty,
        main_character=request.main_character,
        quest_objective=request.quest_objective,
        missions=request.missions,
        ending_preference=request.ending_preference,
        additional_instructions=request.additional_instructions or "",
        image_context=image_context
    )

    result = await nemotron_client.generate_chat_completion(
        system_prompt=QUEST_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        temperature=0.7
    )

    raw_data = result["data"]
    try:
        structured_quest = QuestStructuredContent(
            title=raw_data.get("title", "Untitled Quest"),
            quest_description=raw_data.get("quest_description", ""),
            background_story=raw_data.get("background_story", ""),
            main_character=raw_data.get("main_character", request.main_character),
            npcs=raw_data.get("npcs", ""),
            objectives=raw_data.get("objectives", ""),
            challenges=raw_data.get("challenges", ""),
            dialogue=raw_data.get("dialogue", ""),
            rewards=raw_data.get("rewards", ""),
            ending=raw_data.get("ending", ""),
            suggested_illustration_description=raw_data.get("suggested_illustration_description", "")
        )
    except Exception as e:
        logger.error(f"Failed to validate quest structure: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"AI model output could not be formatted into structured quest: {str(e)}"
        )

    # Record history
    history = GenerationHistory(
        operation_type="QUEST",
        model_name=result["model_used"],
        input_prompt=user_prompt[:2000]
    )
    db.add(history)
    db.commit()

    return QuestResponse(
        success=True,
        data=structured_quest,
        model_used=result["model_used"],
        prompt_tokens=result.get("prompt_tokens")
    )
