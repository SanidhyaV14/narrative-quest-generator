"""
Narrative Studio — Dashboard Page
Adheres to PART 9: A world of stories begins here.
"""

import streamlit as st
from frontend.components.page_header import render_page_header
from frontend.components.statistics import render_archive_statistics
from frontend.components.cards import render_studio_cards
from frontend.components.empty_states import render_empty_state
from frontend.components.search import render_search_bar
from frontend.components.navigation import navigate_to
from frontend.utils.helpers import format_date, get_project_badge_html
from frontend.config import BACKEND_URL

try:
    from frontend.services.api_client import api_client
except (ModuleNotFoundError, ImportError):
    from services.api_client import api_client


def render_dashboard():
    """Renders the Dark Academia literary Dashboard."""
    # 1. Fetch Real Projects from Backend
    try:
        all_projects = api_client.list_projects()
        story_count = sum(1 for p in all_projects if p.get("project_type") == "STORY")
        quest_count = sum(1 for p in all_projects if p.get("project_type") == "GAME_QUEST")
        total_count = len(all_projects)
    except Exception:
        all_projects = []
        story_count, quest_count, total_count = 0, 0, 0

    # 2. Global Archive Search Bar
    filtered_projects = render_search_bar(all_projects)
    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    # 3. Main Hero Banner with dashboard_bg.png
    render_page_header(
        badge="NARRATIVE STUDIO",
        title="A world of stories begins here.",
        subtitle="Your private space for creating stories, building worlds, and exploring visual imagination.",
        bg_asset="dashboard_bg.png",
        overlay_darkness=0.88
    )

    # 4. Three Compact Real Statistics
    render_archive_statistics(
        total_projects=total_count,
        story_count=story_count,
        quest_count=quest_count
    )

    st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)

    # 5. Three Creative Studio Cards
    render_studio_cards()

    st.markdown("<div style='height: 1.8rem;'></div>", unsafe_allow_html=True)

    # 6. Recently in Your Archive Section
    st.markdown("""
        <h2 class="section-title">RECENTLY IN YOUR ARCHIVE</h2>
    """, unsafe_allow_html=True)

    if not all_projects:
        # Elegant Empty State using decorative_illustrations.png
        render_empty_state(
            title="No records cataloged in your archive yet.",
            description="Your literary journey begins with a single idea. Launch one of the creative studios above to compose your first manuscript or RPG quest.",
            cta_label="Compose First Story →",
            on_cta_click=lambda: navigate_to("Story Generator")
        )
    else:
        display_list = filtered_projects if filtered_projects != all_projects else all_projects[:4]

        col_left, col_right = st.columns([2.2, 1])

        with col_left:
            for p in display_list:
                p_id = p.get("id")
                p_type = p.get("project_type")
                p_title = p.get("title")
                p_date = format_date(p.get("updated_at") or p.get("created_at", ""))
                badge_html = get_project_badge_html(p_type)

                with st.container(border=True):
                    c_info, c_action = st.columns([3, 1])
                    with c_info:
                        st.markdown(badge_html, unsafe_allow_html=True)
                        st.markdown(f"<h3 style='margin: 0.2rem 0; font-size: 1.3rem; color: var(--text-primary);'>{p_title}</h3>", unsafe_allow_html=True)
                        st.caption(f"Last modified: {p_date} &bull; Catalog ID: #{p_id}")
                    with c_action:
                        st.write("")
                        if st.button("Open Record →", key=f"dash_rec_{p_id}", use_container_width=True):
                            st.session_state["selected_project_id"] = p_id
                            navigate_to("My Projects")

        with col_right:
            with st.container(border=True):
                st.markdown("""
                    <div style="font-family: var(--font-display); font-size: 1.15rem; color: var(--accent-gold); font-weight: 700; margin-bottom: 0.5rem;">
                        Quick Studio Access
                    </div>
                    <p style="color: var(--parchment); font-size: 0.88rem; font-family: var(--font-reading); line-height: 1.5; margin-bottom: 1rem;">
                        Directly enter an atelier to initiate a new creation or synthesize visual art.
                    </p>
                """, unsafe_allow_html=True)

                if st.button("Compose New Story", key="dash_quick_story", use_container_width=True):
                    navigate_to("Story Generator")
                if st.button("Architect RPG Quest", key="dash_quick_quest", use_container_width=True):
                    navigate_to("Quest Generator")
                if st.button("Synthesize Artwork", key="dash_quick_image", use_container_width=True):
                    navigate_to("Image Studio")
