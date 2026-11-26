"""
Narrative Studio — Asset Resolver & Image Helpers
Handles local asset loading, verification, base64 encoding, and overlays.
"""

import base64
from pathlib import Path
from typing import Optional


def get_project_root() -> Path:
    """Returns the absolute path to the project root directory."""
    # frontend/utils/assets.py -> frontend/utils -> frontend -> root
    return Path(__file__).resolve().parent.parent.parent


def get_asset_path(filename: str) -> Path:
    """Resolves an asset filename relative to the project root assets/ directory."""
    root = get_project_root()
    return root / "assets" / filename


def asset_exists(filename: str) -> bool:
    """Verifies whether an asset file exists on disk."""
    return get_asset_path(filename).is_file()


def get_asset_base64(filename: str) -> str:
    """
    Reads an asset file from assets/ and returns a base64 data URI string.
    Returns an empty string if the file is missing.
    """
    path = get_asset_path(filename)
    if not path.is_file():
        # Fallback check directly in relative path
        alt_path = Path("assets") / filename
        if alt_path.is_file():
            path = alt_path
        else:
            return ""

    try:
        with open(path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
            suffix = path.suffix.lower().replace(".", "")
            mime = "image/png" if suffix == "png" else "image/jpeg" if suffix in ("jpg", "jpeg") else "image/webp"
            return f"data:{mime};base64,{encoded}"
    except Exception:
        return ""


def get_hero_bg_style(filename: str, overlay_darkness: float = 0.85) -> str:
    """
    Generates an inline CSS background property with a controlled dark overlay.
    Gracefully falls back to solid dark academic canvas if asset is missing.
    """
    b64 = get_asset_base64(filename)
    if b64:
        # Dual-layer dark gradient overlay for optimal legibility
        return (
            f"background-image: linear-gradient(180deg, rgba(17, 19, 15, {overlay_darkness - 0.3:.2f}) 0%, "
            f"rgba(17, 19, 15, {overlay_darkness:.2f}) 80%, rgba(17, 19, 15, 0.98) 100%), "
            f"url('{b64}'); background-size: cover; background-position: center;"
        )
    return "background-color: var(--bg-card); border: 1px solid var(--border-color);"


def get_decorative_divider_html(width: str = "180px", opacity: float = 0.6) -> str:
    """
    Renders a centered decorative accent divider using an elegant antique gold ornament.
    Returns compact single-line HTML without indentation to prevent markdown code block parsing.
    """
    return '<div style="text-align: center; margin: 1.2rem 0; color: var(--accent-gold); opacity: 0.8; font-size: 1.1rem; letter-spacing: 0.4em;">✦ &nbsp; ⚜ &nbsp; ✦</div>'
