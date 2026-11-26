import io
import pytest
from PIL import Image
from unittest.mock import AsyncMock, patch


def test_workflow_a_text_to_story_to_image(client):
    """
    WORKFLOW A: TEXT-TO-STORY-TO-IMAGE
    1. User logs in (or registers).
    2. User enters story details.
    3. Nemotron generates the story.
    4. Image prompt is created.
    5. FLUX generates an illustration.
    6. User saves the project.
    7. User retrieves it from My Projects and exports TXT.
    """
    # 1. Register & Login
    reg_resp = client.post("/api/auth/register", json={
        "username": "workflow_author",
        "email": "author_wf_a@example.com",
        "password": "password123",
        "confirm_password": "password123"
    })
    token = reg_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2 & 3. Generate story with Nemotron
    with patch("backend.routes.generation.nemotron_client.generate_chat_completion", new_callable=AsyncMock) as mock_story:
        mock_story.return_value = {
            "data": {
                "title": "Chronicles of the Starforged Realm",
                "genre": "Science Fiction",
                "introduction": "The stars flickered over the crystalline domes of Kepler-9.",
                "main_characters": "Commander Rayne",
                "setting": "An abandoned orbital observatory",
                "conflict": "Solar flares threaten the atmospheric grid",
                "complete_story": "Rayne calibrated the pulse emitters as the coronal mass ejection peaked...",
                "ending": "The shield stabilized, casting a prismatic glow across the colony.",
                "suggested_image_description": "A sci-fi orbital observatory overlooking a vibrant nebula, digital concept art"
            },
            "model_used": "nvidia/nemotron-3.5-super-vl-120b-a12b"
        }

        story_resp = client.post("/api/generate/story", json={
            "genre": "Science Fiction",
            "theme": "Survival",
            "setting": "An abandoned orbital observatory",
            "main_character": "Commander Rayne",
            "story_idea": "Protecting a space colony from solar storms",
            "story_length": "Medium",
            "tone": "Suspenseful"
        }, headers=headers)
        assert story_resp.status_code == 200
        story_data = story_resp.json()["data"]

    # 4 & 5. Generate illustration with FLUX
    with patch("backend.routes.images.flux_client.generate_image", new_callable=AsyncMock) as mock_flux:
        mock_flux.return_value = {
            "image_path": "uploads/generated/starforged_nebula.png",
            "prompt_used": story_data["suggested_image_description"],
            "model_used": "black-forest-labs/flux.1-dev"
        }

        img_resp = client.post("/api/images/generate", json={
            "prompt": story_data["suggested_image_description"],
            "art_style": "Concept art",
            "mood": "Dramatic"
        }, headers=headers)
        assert img_resp.status_code == 200
        img_path = img_resp.json()["image_path"]

    # 6. Save Project
    save_resp = client.post("/api/projects", json={
        "title": story_data["title"],
        "project_type": "STORY",
        "input_data": {"genre": "Science Fiction", "theme": "Survival"},
        "generated_content": story_data,
        "image_paths": [img_path],
        "image_prompt": story_data["suggested_image_description"]
    }, headers=headers)
    assert save_resp.status_code == 201
    proj_id = save_resp.json()["id"]

    # 7. Retrieve from My Projects & Export TXT
    list_resp = client.get("/api/projects", headers=headers)
    assert list_resp.status_code == 200
    assert any(p["id"] == proj_id for p in list_resp.json()["projects"])

    export_resp = client.get(f"/api/projects/{proj_id}/export", headers=headers)
    assert export_resp.status_code == 200
    assert "Chronicles of the Starforged Realm" in export_resp.text
    assert "uploads/generated/starforged_nebula.png" in export_resp.text


def test_workflow_b_image_to_understanding_to_story(client):
    """
    WORKFLOW B: IMAGE-TO-UNDERSTANDING-TO-STORY
    1. User uploads an image.
    2. Nemotron analyzes the image.
    3. Displays image description and elements.
    4. User generates a story inspired by that image.
    5. Saves project.
    """
    # 1. Login
    reg_resp = client.post("/api/auth/register", json={
        "username": "vision_seeker",
        "email": "vision_wf_b@example.com",
        "password": "password123",
        "confirm_password": "password123"
    })
    token = reg_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create dummy PNG image bytes
    buf = io.BytesIO()
    Image.new("RGB", (64, 64), color="darkgreen").save(buf, format="PNG")
    img_bytes = buf.getvalue()

    # 2 & 3. Analyze image with Nemotron Vision
    with patch("backend.routes.images.nemotron_client.analyze_image_with_vision", new_callable=AsyncMock) as mock_vis:
        mock_vis.return_value = {
            "data": {
                "description": "An ancient moss-covered stone archway deep within a twilight jungle.",
                "visible_characters": "A lone explorer with an enchanted compass.",
                "objects": "Runic glyphs carved into granite stones.",
                "environment": "Humid subtropical canopy with glowing bioluminescent fungi.",
                "colors_and_atmosphere": "Deep emerald greens, mysterious cyan luminescence.",
                "possible_themes": "Ancient Mysteries, Nature reclaiming Civilization.",
                "story_ideas": "The Gate of the Jade Serpent."
            },
            "model_used": "meta/llama-3.2-11b-vision-instruct"
        }

        analyze_resp = client.post(
            "/api/images/analyze",
            files={"file": ("jungle_gate.png", img_bytes, "image/png")},
            data={"question": "What secrets lie beyond this arch?"},
            headers=headers
        )
        assert analyze_resp.status_code == 200
        vis_analysis = analyze_resp.json()
        saved_img_path = vis_analysis["image_path"]

    # 4. Generate story inspired by the analyzed image
    with patch("backend.routes.generation.nemotron_client.generate_chat_completion", new_callable=AsyncMock) as mock_story:
        mock_story.return_value = {
            "data": {
                "title": "The Gate of the Jade Serpent",
                "genre": "Adventure",
                "introduction": "Beyond the mossy arch, time stood still.",
                "main_characters": "Alan, an antiquities scout",
                "setting": "Twilight jungle canopy",
                "conflict": "The gateway demands an emerald token",
                "complete_story": "Alan adjusted his torch. The jade runes began to awaken...",
                "ending": "The threshold opened into the lost temple of the serpent kings.",
                "suggested_image_description": "An adventurer stepping through a glowing emerald jungle gate"
            },
            "model_used": "nvidia/nemotron-3.5-super-vl-120b-a12b"
        }

        story_resp = client.post("/api/generate/story", json={
            "genre": "Adventure",
            "theme": "Mystery",
            "setting": vis_analysis["environment"],
            "main_character": "Alan, an antiquities scout",
            "story_idea": vis_analysis["story_ideas"],
            "story_length": "Short",
            "tone": "Suspenseful",
            "reference_image_path": saved_img_path
        }, headers=headers)
        assert story_resp.status_code == 200
        story_content = story_resp.json()["data"]

    # 5. Save Project with reference image
    save_resp = client.post("/api/projects", json={
        "title": story_content["title"],
        "project_type": "STORY",
        "input_data": {"visual_inspiration": vis_analysis["description"]},
        "generated_content": story_content,
        "image_paths": [saved_img_path]
    }, headers=headers)
    assert save_resp.status_code == 201
    assert len(save_resp.json()["images"]) == 1
    assert save_resp.json()["images"][0]["image_type"] == "UPLOAD"


def test_workflow_c_text_to_game_quest_to_image(client):
    """
    WORKFLOW C: TEXT-TO-GAME-QUEST-TO-IMAGE
    1. User enters game quest details.
    2. Nemotron generates structured game quest.
    3. FLUX generates illustration.
    4. User saves and submits feedback.
    """
    reg_resp = client.post("/api/auth/register", json={
        "username": "quest_architect",
        "email": "architect_wf_c@example.com",
        "password": "password123",
        "confirm_password": "password123"
    })
    token = reg_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Generate Quest
    with patch("backend.routes.generation.nemotron_client.generate_chat_completion", new_callable=AsyncMock) as mock_quest:
        mock_quest.return_value = {
            "data": {
                "title": "Lair of the Frostfang Wyrm",
                "quest_description": "Ascend the Frozen Spire and claim the Wyrm's Glacial Core.",
                "background_story": "A legendary ice wyrm has awakened, freezing trade caravans across the pass.",
                "main_character": "Valen the Pyromancer",
                "npcs": "Mayor Donald, Blacksmith Greta",
                "objectives": "1. Gather fire-bloom moss.\n2. Scale Frostfang Pass.\n3. Slay the Wyrm.",
                "challenges": "Blizzards, falling avalanches, sub-zero hypothermia timer.",
                "dialogue": "Donald: 'Bring back the core, or the town freezes before midwinter.'",
                "rewards": "2500 XP, Glacial Staff of Winter, 800 Gold",
                "ending": "The pass thaws, restoring travel between the mountain kingdoms.",
                "suggested_illustration_description": "A fiery pyromancer facing a massive crystalline ice dragon on a frozen peak"
            },
            "model_used": "nvidia/nemotron-3.5-super-vl-120b-a12b"
        }

        quest_resp = client.post("/api/generate/quest", json={
            "game_genre": "RPG",
            "theme": "Rescue",
            "setting": "Frostfang Mountain Pass",
            "difficulty": "Hard",
            "main_character": "Valen the Pyromancer",
            "quest_objective": "Slay the Wyrm and reclaim the pass",
            "missions": 3,
            "ending_preference": "Victory"
        }, headers=headers)
        assert quest_resp.status_code == 200
        quest_data = quest_resp.json()["data"]

    # 3. Generate Quest Illustration
    with patch("backend.routes.images.flux_client.generate_image", new_callable=AsyncMock) as mock_flux:
        mock_flux.return_value = {
            "image_path": "uploads/generated/frostfang_wyrm.png",
            "prompt_used": quest_data["suggested_illustration_description"],
            "model_used": "black-forest-labs/flux.1-dev"
        }

        img_resp = client.post("/api/images/generate", json={
            "prompt": quest_data["suggested_illustration_description"],
            "art_style": "Fantasy illustration",
            "mood": "Epic"
        }, headers=headers)
        assert img_resp.status_code == 200
        quest_img_path = img_resp.json()["image_path"]

    # 4. Save and Submit Feedback
    save_resp = client.post("/api/projects", json={
        "title": quest_data["title"],
        "project_type": "GAME_QUEST",
        "input_data": {"difficulty": "Hard", "missions": 3},
        "generated_content": quest_data,
        "image_paths": [quest_img_path],
        "image_prompt": quest_data["suggested_illustration_description"]
    }, headers=headers)
    assert save_resp.status_code == 201
    proj_id = save_resp.json()["id"]

    fb_resp = client.post("/api/feedback", json={
        "project_id": proj_id,
        "rating": 5,
        "comments": "Superb quest structure with balanced rewards and vivid dialogue!"
    }, headers=headers)
    assert fb_resp.status_code == 201
    assert fb_resp.json()["rating"] == 5
