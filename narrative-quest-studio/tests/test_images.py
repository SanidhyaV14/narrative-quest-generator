import io
import pytest
from PIL import Image
from unittest.mock import AsyncMock, patch


def create_test_image_bytes(format="PNG", size=(100, 100), color="blue"):
    buf = io.BytesIO()
    img = Image.new("RGB", size, color=color)
    img.save(buf, format=format)
    return buf.getvalue()


def test_tc07_upload_valid_image(client, auth_headers):
    """TC07: Upload a valid image."""
    img_bytes = create_test_image_bytes(format="PNG")

    with patch("backend.routes.images.nemotron_client.analyze_image_with_vision", new_callable=AsyncMock) as mock_vision:
        mock_vision.return_value = {
            "data": {
                "description": "A clear blue square image",
                "visible_characters": "None",
                "objects": "Blue canvas",
                "environment": "Minimalist digital space",
                "colors_and_atmosphere": "Cool blue, tranquil",
                "possible_themes": "Simplicity",
                "story_ideas": "A realm of pure azure."
            },
            "model_used": "meta/llama-3.2-11b-vision-instruct"
        }

        response = client.post(
            "/api/images/analyze",
            files={"file": ("test.png", img_bytes, "image/png")},
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "uploads/references/" in data["image_path"]
        assert data["description"] == "A clear blue square image"


def test_tc08_reject_invalid_image(client, auth_headers):
    """TC08: Reject an invalid image (non-image bytes or invalid extension)."""
    fake_bytes = b"This is a text file masquerading as an image."
    response = client.post(
        "/api/images/analyze",
        files={"file": ("test.txt", fake_bytes, "text/plain")},
        headers=auth_headers
    )
    assert response.status_code == 400


def test_tc09_reject_oversized_image(client, auth_headers):
    """TC09: Reject an image larger than 5 MB."""
    # 5.5 MB of dummy data
    oversized_bytes = b"\x00" * (6 * 1024 * 1024)
    response = client.post(
        "/api/images/analyze",
        files={"file": ("huge.png", oversized_bytes, "image/png")},
        headers=auth_headers
    )
    assert response.status_code == 400
    assert "exceeds the maximum" in response.json()["detail"]


def test_tc10_analyze_uploaded_image(client, auth_headers):
    """TC10: Analyze an uploaded image."""
    img_bytes = create_test_image_bytes(format="JPEG")

    with patch("backend.routes.images.nemotron_client.analyze_image_with_vision", new_callable=AsyncMock) as mock_vision:
        mock_vision.return_value = {
            "data": {
                "description": "An ancient stone tower in mountain mist",
                "visible_characters": "A lonely sentinel",
                "objects": "Watchfire, stone steps",
                "environment": "Rugged alpine crags",
                "colors_and_atmosphere": "Moody greys and ambers",
                "possible_themes": "Vigilance",
                "story_ideas": "The Last Beacon"
            },
            "model_used": "meta/llama-3.2-11b-vision-instruct"
        }

        response = client.post(
            "/api/images/analyze",
            files={"file": ("tower.jpg", img_bytes, "image/jpeg")},
            data={"question": "What lore does this scene inspire?"},
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["visible_characters"] == "A lonely sentinel"
        assert data["story_ideas"] == "The Last Beacon"


def test_tc11_generate_illustration(client, auth_headers):
    """TC11: Generate an illustration."""
    with patch("backend.routes.images.flux_client.generate_image", new_callable=AsyncMock) as mock_gen:
        mock_gen.return_value = {
            "image_path": "uploads/generated/mock_illustration.png",
            "prompt_used": "A glowing crystal cave, Fantasy illustration",
            "model_used": "black-forest-labs/flux.1-dev"
        }

        response = client.post(
            "/api/images/generate",
            json={
                "prompt": "A glowing crystal cave",
                "art_style": "Fantasy illustration",
                "mood": "Mysterious"
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["image_path"] == "uploads/generated/mock_illustration.png"
