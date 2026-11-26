"""
Narrative Studio — Helper Functions & Utilities
"""

from datetime import datetime


def format_date(date_str: str) -> str:
    """Formats an ISO timestamp or date string into an elegant literary date."""
    if not date_str:
        return "Unknown Date"
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return dt.strftime("%B %d, %Y")
    except Exception:
        # Fallback for simple date strings like "2026-11-26"
        return date_str[:10]


def truncate_text(text: str, max_chars: int = 140) -> str:
    """Truncates text with an ellipsis if it exceeds max_chars."""
    if not text:
        return ""
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + "..."


def get_project_badge_html(project_type: str) -> str:
    """Returns an editorial badge HTML for story or quest."""
    if project_type == "STORY":
        return "<span class='badge-tag badge-bronze' style='font-family: var(--font-sans); color: var(--bronze); font-weight: 700; letter-spacing: 0.12em;'>MANUSCRIPT</span>"
    elif project_type == "GAME_QUEST":
        return "<span class='badge-tag badge-olive' style='font-family: var(--font-sans); color: var(--accent-olive); font-weight: 700; letter-spacing: 0.12em;'>QUEST CODEX</span>"
    return f"<span class='badge-tag badge-gold' style='font-family: var(--font-sans); color: var(--accent-gold); font-weight: 700; letter-spacing: 0.12em;'>{project_type}</span>"
