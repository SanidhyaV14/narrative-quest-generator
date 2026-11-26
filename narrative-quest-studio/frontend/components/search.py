import streamlit as st
from typing import List, Dict, Any


def render_search_bar(projects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Renders a global search bar querying accessible real projects."""
    query = st.text_input(
        "Search your creative archive",
        placeholder="Search projects by title, genre, character, or setting...",
        key="global_search_input"
    )

    if not query:
        return projects

    q = query.lower().strip()
    filtered = []
    for p in projects:
        title = (p.get("title") or "").lower()
        ptype = (p.get("project_type") or "").lower()
        content = p.get("generated_content", {})
        genre = str(content.get("genre", "")).lower()
        character = str(content.get("main_characters", "") or content.get("main_character", "")).lower()
        setting = str(content.get("setting", "")).lower()
        story_body = str(content.get("complete_story", "") or content.get("quest_description", "")).lower()

        if any(q in field for field in (title, ptype, genre, character, setting, story_body)):
            filtered.append(p)

    st.caption(f"Found {len(filtered)} project(s) matching '{query}'")
    return filtered
