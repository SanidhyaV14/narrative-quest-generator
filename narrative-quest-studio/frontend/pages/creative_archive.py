import streamlit as st
from frontend.config import BACKEND_URL
from frontend.utils.assets import get_asset_base64 as get_image_base64
from frontend.components.navigation import render_back_button, navigate_to

try:
    from frontend.services.api_client import api_client
except (ModuleNotFoundError, ImportError):
    from services.api_client import api_client


def render_creative_archive():
    """Renders the curated private library gallery (Creative Archive)."""
    render_back_button(current_page="Creative Archive", section="Library")

    bg_b64 = get_image_base64("assets/images/creative_archive_bg.webp")
    bg_style = f"background-image: linear-gradient(180deg, rgba(21, 23, 19, 0.82) 0%, rgba(21, 23, 19, 0.96) 100%), url('{bg_b64}'); background-size: cover;" if bg_b64 else ""

    st.markdown(f"""
        <div style="{bg_style} border-radius: 8px; padding: 2rem; margin-bottom: 2rem; border: 1px solid var(--border-subtle);">
            <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.15em; color: var(--accent-gold); font-weight: 600; margin-bottom: 0.3rem;">
                CURATED REPOSITORY &bull; PERMANENT COLLECTIONS
            </div>
            <h1 style="margin: 0; color: var(--text-ivory);">Creative Archive</h1>
            <p style="font-family: var(--font-serif); font-style: italic; color: var(--text-cream); font-size: 1.15rem; margin-top: 0.25rem;">
                "A grand repository of manuscripts, quest codices, and visual lore."
            </p>
        </div>
    """, unsafe_allow_html=True)

    try:
        projects = api_client.list_projects()
    except Exception:
        projects = []

    tab_stories, tab_quests, tab_gallery = st.tabs(["Story Anthology", "Quest Codex", "Gallery of Visions"])

    # 1. Story Anthology
    with tab_stories:
        stories = [p for p in projects if p.get("project_type") == "STORY"]
        if not stories:
            st.info("No manuscripts recorded in the anthology yet. Use Story Studio to author one.")
        else:
            for s in stories:
                c = s.get("generated_content", {})
                with st.container(border=True):
                    st.markdown(f"<span class='studio-card-tag tag-terracotta'>MANUSCRIPT</span>", unsafe_allow_html=True)
                    st.markdown(f"<h3 style='margin: 0.2rem 0; color: var(--text-ivory);'>{s.get('title')}</h3>", unsafe_allow_html=True)
                    st.caption(f"Genre: {c.get('genre', 'Unknown')} &bull; Date: {s.get('created_at', '')[:10]}")
                    st.write(c.get("introduction", ""))
                    if st.button(f"Read Full Manuscript →", key=f"read_s_{s.get('id')}"):
                        st.session_state["selected_project_id"] = s.get("id")
                        navigate_to("My Projects")

    # 2. Quest Codex
    with tab_quests:
        quests = [p for p in projects if p.get("project_type") == "GAME_QUEST"]
        if not quests:
            st.info("No quest codices cataloged yet. Use Quest Studio to architect one.")
        else:
            for q in quests:
                c = q.get("generated_content", {})
                with st.container(border=True):
                    st.markdown(f"<span class='studio-card-tag tag-sage'>RPG CODEX</span>", unsafe_allow_html=True)
                    st.markdown(f"<h3 style='margin: 0.2rem 0; color: var(--text-ivory);'>{q.get('title')}</h3>", unsafe_allow_html=True)
                    st.caption(f"Archived on {q.get('created_at', '')[:10]}")
                    st.write(c.get("quest_description", ""))
                    if st.button(f"Inspect Quest Objectives →", key=f"insp_q_{q.get('id')}"):
                        st.session_state["selected_project_id"] = q.get("id")
                        navigate_to("My Projects")

    # 3. Gallery of Visions
    with tab_gallery:
        all_images = []
        for p in projects:
            for img in p.get("images", []):
                all_images.append({
                    "project_title": p.get("title"),
                    "file_path": img.get("file_path"),
                    "type": img.get("image_type"),
                    "prompt": img.get("image_prompt")
                })

        if not all_images:
            st.info("No artwork illustrations archived yet. Generate illustrations via Story, Quest, or Image Studio.")
        else:
            img_grid = st.columns(3)
            for idx, img_data in enumerate(all_images):
                with img_grid[idx % 3]:
                    with st.container(border=True):
                        i_path = img_data.get("file_path") or img_data.get("image_path") or ""
                        img_url = f"{BACKEND_URL}/{i_path}"
                        st.image(img_url, use_container_width=True)
                        st.markdown(f"<div style='font-size: 0.85rem; font-weight: 600; color: var(--text-ivory);'>{img_data['project_title']}</div>", unsafe_allow_html=True)
                        st.caption(f"Type: {img_data['type']}")
