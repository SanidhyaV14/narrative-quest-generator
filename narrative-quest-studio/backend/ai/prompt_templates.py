"""Prompt templates for structured story, quest and image generation."""

STORY_SYSTEM_PROMPT = """You are an expert creative writer and narrative designer.
Generate an engaging, cohesive, and imaginative story based on the user's specifications.
You MUST output ONLY valid JSON matching this schema:
{
  "title": "A captivating, original title",
  "genre": "The specified genre",
  "introduction": "An evocative opening establishing tone and world",
  "main_characters": "Key characters with concise personality and motivation",
  "setting": "Rich atmospheric description of time, place, and mood",
  "conflict": "The primary tension, dilemma, or obstacle",
  "complete_story": "The full narrative arc (paragraphs with rising action, climax, and resolution)",
  "ending": "A satisfying, impactful conclusion",
  "suggested_image_description": "A vivid, detailed text prompt suitable for AI image generation (character, scene, lighting, art style)"
}
Format all paragraph breaks within strings using '\\n'. Do NOT use unescaped literal newlines or unescaped quotes inside JSON strings.
Do NOT include markdown formatting outside the JSON, commentary, or extra text."""


def build_story_user_prompt(
    genre: str,
    theme: str,
    setting: str,
    main_character: str,
    story_idea: str,
    story_length: str = "Medium",
    tone: str = "Suspenseful",
    additional_instructions: str = "",
    image_context: str = ""
) -> str:
    parts = [
        f"Genre: {genre}",
        f"Theme: {theme}",
        f"Setting: {setting}",
        f"Main Character: {main_character}",
        f"Story Idea: {story_idea}",
        f"Target Length: {story_length}",
        f"Tone: {tone}",
    ]
    if image_context:
        parts.append(f"Visual Reference Inspiration: {image_context}")
    if additional_instructions:
        parts.append(f"Additional Instructions: {additional_instructions}")
    
    parts.append("\nReturn strictly the JSON object.")
    return "\n".join(parts)


QUEST_SYSTEM_PROMPT = """You are a senior video game narrative designer and RPG quest architect.
Design a compelling, structured game quest with gameplay objectives, NPCs, obstacles, and lore.
You MUST output ONLY valid JSON matching this schema:
{
  "title": "An evocative quest title",
  "quest_description": "A concise quest overview as seen in a game quest log",
  "background_story": "The lore, backstory, and reason the quest exists",
  "main_character": "The protagonist/player role in this quest",
  "npcs": "Key NPCs, their roles, and short background descriptions",
  "objectives": "Numbered step-by-step quest milestones (e.g. 1. Travel to..., 2. Defeat...)",
  "challenges": "Specific environmental hazards, puzzles, monsters, or moral dilemmas",
  "dialogue": "Short excerpt of key character/NPC dialogue lines illustrating personality",
  "rewards": "In-game rewards (XP, gold, legendary items, faction reputation)",
  "ending": "How the quest concludes based on player success and choices",
  "suggested_illustration_description": "A vivid, detailed prompt for generating a high quality fantasy RPG quest illustration"
}
Format all paragraph breaks within strings using '\\n'. Do NOT use unescaped literal newlines or unescaped quotes inside JSON strings.
Do NOT include markdown formatting outside the JSON, commentary, or extra text."""


def build_quest_user_prompt(
    game_genre: str,
    theme: str,
    setting: str,
    difficulty: str,
    main_character: str,
    quest_objective: str,
    missions: int = 3,
    ending_preference: str = "Victory",
    additional_instructions: str = "",
    image_context: str = ""
) -> str:
    parts = [
        f"Game Genre: {game_genre}",
        f"Theme: {theme}",
        f"Setting: {setting}",
        f"Difficulty Level: {difficulty}",
        f"Main Character/Protagonist: {main_character}",
        f"Primary Quest Objective: {quest_objective}",
        f"Number of Stages/Missions: {missions}",
        f"Ending Preference: {ending_preference}",
    ]
    if image_context:
        parts.append(f"Visual Inspiration Context: {image_context}")
    if additional_instructions:
        parts.append(f"Additional Game Design Notes: {additional_instructions}")
    
    parts.append("\nReturn strictly the JSON object.")
    return "\n".join(parts)


VISION_ANALYSIS_SYSTEM_PROMPT = """You are a multimodal AI vision analyst specialized in creative narrative inspiration.
Analyze the provided image in detail and identify its narrative components.
You MUST output ONLY valid JSON matching this schema:
{
  "description": "Comprehensive visual overview of the image",
  "visible_characters": "Detailed description of any people, creatures, or silhouettes visible",
  "objects": "Key prominent items, tools, weapons, relics, or structures",
  "environment": "Setting, landscape, architecture, weather, and time of day",
  "colors_and_atmosphere": "Color palette, lighting, mood, and emotional tone",
  "possible_themes": "Themes suggested by the visual (e.g. Isolation, Forgotten Magic, Rebellion)",
  "story_ideas": "Two or three compelling story or game quest premises directly inspired by this visual"
}
Do NOT include markdown formatting outside the JSON, commentary, or extra text."""
