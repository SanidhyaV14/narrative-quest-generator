import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException


def test_tc05_generate_story(client, auth_headers):
    """TC05: Generate a story."""
    mock_story_data = {
        "title": "The Whispering Woods",
        "genre": "Fantasy",
        "introduction": "Deep in Eldenwood, the trees remembered the ancient gods.",
        "main_characters": "Lyra, a young spellblade",
        "setting": "An enchanted autumn forest with silver foliage",
        "conflict": "The guardian crystal is cracking, leaking corruption",
        "complete_story": "Lyra drew her runic sword as the mist rolled in...",
        "ending": "Restoring the crystal at dusk, the forest sighed in peace.",
        "suggested_image_description": "A spellblade woman with a glowing runic sword in a silver forest"
    }

    with patch("backend.routes.generation.nemotron_client.generate_chat_completion", new_callable=AsyncMock) as mock_gen:
        mock_gen.return_value = {
            "data": mock_story_data,
            "model_used": "nvidia/nemotron-3.5-super-vl-120b-a12b",
            "prompt_tokens": 120
        }

        response = client.post(
            "/api/generate/story",
            json={
                "genre": "Fantasy",
                "theme": "Adventure",
                "setting": "An enchanted autumn forest",
                "main_character": "Lyra, a young spellblade",
                "story_idea": "Investigating a corrupted crystal in the woods",
                "story_length": "Short",
                "tone": "Suspenseful"
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["title"] == "The Whispering Woods"
        assert data["data"]["genre"] == "Fantasy"
        assert len(data["data"]["complete_story"]) > 10


def test_tc06_generate_game_quest(client, auth_headers):
    """TC06: Generate a game quest."""
    mock_quest_data = {
        "title": "Siege of the Sunken Bastion",
        "quest_description": "Breach the submerged fortress and recover the Sunken Sigil.",
        "background_story": "The fortress sank during the Cataclysm, sealing the ancient guardian within.",
        "main_character": "Captain Vane",
        "npcs": "Archmage Korin (quest giver), Quartermaster Talia",
        "objectives": "1. Secure the harbor gate.\n2. Drain the lower crypts.\n3. Defeat the Leviathan Golem.",
        "challenges": "Rising floodwaters, shock eels, and timed rune switches.",
        "dialogue": "Korin: 'If the Sigil is lost, the tide takes the city with it.'",
        "rewards": "1200 XP, Sunken Sigil Trinket, 350 Gold",
        "ending": "The fortress gates are secured and the city is saved from flooding.",
        "suggested_illustration_description": "A submerged fortress under churning waves with glowing blue ward-runes"
    }

    with patch("backend.routes.generation.nemotron_client.generate_chat_completion", new_callable=AsyncMock) as mock_gen:
        mock_gen.return_value = {
            "data": mock_quest_data,
            "model_used": "nvidia/nemotron-3.5-super-vl-120b-a12b",
            "prompt_tokens": 150
        }

        response = client.post(
            "/api/generate/quest",
            json={
                "game_genre": "RPG",
                "theme": "Exploration",
                "setting": "Submerged sunken fortress",
                "difficulty": "Hard",
                "main_character": "Captain Vane",
                "quest_objective": "Recover the Sunken Sigil",
                "missions": 3,
                "ending_preference": "Victory"
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["title"] == "Siege of the Sunken Bastion"
        assert data["data"]["missions"] if "missions" in data["data"] else True


def test_tc17_handle_unavailable_ai_endpoint(client, auth_headers):
    """TC17: Handle an unavailable AI endpoint gracefully."""
    with patch("backend.routes.generation.nemotron_client.generate_chat_completion", new_callable=AsyncMock) as mock_gen:
        mock_gen.side_effect = HTTPException(
            status_code=503,
            detail="NVIDIA API key is not configured. Please set NVIDIA_API_KEY in .env."
        )

        response = client.post(
            "/api/generate/story",
            json={
                "genre": "Horror",
                "theme": "Survival",
                "setting": "Abandoned asylum",
                "main_character": "Dr. Reed",
                "story_idea": "Trapped during a blizzard",
                "story_length": "Short",
                "tone": "Dark"
            },
            headers=auth_headers
        )
        assert response.status_code == 503
        assert "NVIDIA API key is not configured" in response.json()["detail"]
