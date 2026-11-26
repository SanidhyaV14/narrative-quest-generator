"""
Narrative Studio — Creative Studio Cards & Project Card Components
"""

import streamlit as st
from frontend.utils.assets import get_asset_base64
from frontend.components.navigation import navigate_to


def render_studio_cards():
    """Renders the 3 equal-height Creative Studio feature cards."""
    st.markdown("""
        <div style="margin: 2rem 0 1rem 0;">
            <h2 class="section-title" style="margin: 0; border: none; font-size: 1.65rem;">YOUR CREATIVE LIBRARY</h2>
            <p style="color: var(--text-muted); font-size: 0.95rem; margin-top: 0.2rem; font-family: var(--font-reading);">
                Select an atelier to compose your next manuscript, design an RPG quest, or explore visual art.
            </p>
        </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    story_b64 = get_asset_base64("story_bg.png")
    quest_b64 = get_asset_base64("quest_bg.png")
    image_b64 = get_asset_base64("image_studio_bg.png")

    # 1. STORY GENERATOR CARD
    with c1:
        st.markdown(f"""
            <div class="studio-feature-card" style="background-image: linear-gradient(180deg, rgba(36, 39, 31, 0.85) 0%, rgba(36, 39, 31, 0.98) 100%), url('{story_b64}');">
                <div class="studio-card-inner">
                    <span class="badge-tag badge-bronze">ATELIER I &bull; LITERARY CREATION</span>
                    <div style="font-family: var(--font-display); font-size: 1.45rem; font-weight: 700; color: var(--text-primary); margin-top: 0.2rem;">
                        Story Generator
                    </div>
                    <p style="color: var(--parchment); font-size: 0.92rem; line-height: 1.55; margin-top: 0.5rem; font-family: var(--font-reading);">
                        Craft immersive narratives, memorable characters, and extraordinary fictional worlds.
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Launch Story Generator →", key="btn_card_story", use_container_width=True):
            navigate_to("Story Generator")

    # 2. QUEST GENERATOR CARD
    with c2:
        st.markdown(f"""
            <div class="studio-feature-card" style="background-image: linear-gradient(180deg, rgba(36, 39, 31, 0.85) 0%, rgba(36, 39, 31, 0.98) 100%), url('{quest_b64}');">
                <div class="studio-card-inner">
                    <span class="badge-tag badge-olive">ATELIER II &bull; WORLD-BUILDING</span>
                    <div style="font-family: var(--font-display); font-size: 1.45rem; font-weight: 700; color: var(--text-primary); margin-top: 0.2rem;">
                        Quest Generator
                    </div>
                    <p style="color: var(--parchment); font-size: 0.92rem; line-height: 1.55; margin-top: 0.5rem; font-family: var(--font-reading);">
                        Build structured adventures with objectives, characters, encounters, rewards, and lore.
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Launch Quest Generator →", key="btn_card_quest", use_container_width=True):
            navigate_to("Quest Generator")

    # 3. IMAGE STUDIO CARD
    with c3:
        st.markdown(f"""
            <div class="studio-feature-card" style="background-image: linear-gradient(180deg, rgba(36, 39, 31, 0.85) 0%, rgba(36, 39, 31, 0.98) 100%), url('{image_b64}');">
                <div class="studio-card-inner">
                    <span class="badge-tag badge-gold">ATELIER III &bull; VISUAL ARTS</span>
                    <div style="font-family: var(--font-display); font-size: 1.45rem; font-weight: 700; color: var(--text-primary); margin-top: 0.2rem;">
                        Image Studio
                    </div>
                    <p style="color: var(--parchment); font-size: 0.92rem; line-height: 1.55; margin-top: 0.5rem; font-family: var(--font-reading);">
                        Explore visual references, analyze imagery, and create original illustrations.
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Launch Image Studio →", key="btn_card_image", use_container_width=True):
            navigate_to("Image Studio")
