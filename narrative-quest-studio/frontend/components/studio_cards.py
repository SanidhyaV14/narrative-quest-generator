import streamlit as st
from frontend.utils.assets import get_asset_base64 as get_image_base64
from frontend.components.navigation import navigate_to


def render_studio_cards():
    """Renders the 3 equal-height Creative Studio feature cards."""
    st.markdown("""
        <div style="margin: 2rem 0 1rem 0;">
            <h2 style="margin: 0; border: none; font-size: 1.65rem;">Creative Studios</h2>
            <p style="color: var(--text-muted); font-size: 0.95rem; margin-top: 0.2rem; font-family: var(--font-serif);">
                Select an atelier to craft your next manuscript, quest blueprint, or visual work.
            </p>
        </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    story_bg_b64 = get_image_base64("assets/images/story_studio_bg.webp")
    quest_bg_b64 = get_image_base64("assets/images/quest_studio_bg.webp")
    image_bg_b64 = get_image_base64("assets/images/image_studio_bg.webp")

    # 1. Story Studio Card
    with c1:
        st.markdown(f"""
            <div class="studio-card" style="background-image: linear-gradient(180deg, rgba(37, 40, 32, 0.75) 0%, rgba(37, 40, 32, 0.95) 100%), url('{story_bg_b64}'); background-size: cover;">
                <div>
                    <div class="studio-card-tag tag-terracotta">ATELIER I &bull; NARRATIVE</div>
                    <div style="font-family: var(--font-display); font-size: 1.45rem; font-weight: 600; color: var(--text-ivory);">Story Studio</div>
                    <div style="font-family: var(--font-serif); font-style: italic; font-size: 0.95rem; color: var(--accent-terracotta); margin-bottom: 0.6rem;">"Write. Imagine. Create."</div>
                    <p style="color: var(--text-cream); font-size: 0.92rem; line-height: 1.5; font-family: var(--font-serif);">
                        Craft immersive multi-genre stories with memorable characters, atmospheric settings, and narrative arcs.
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Start Writing →", key="btn_card_story", use_container_width=True):
            navigate_to("Story Studio")

    # 2. Quest Studio Card
    with c2:
        st.markdown(f"""
            <div class="studio-card" style="background-image: linear-gradient(180deg, rgba(37, 40, 32, 0.75) 0%, rgba(37, 40, 32, 0.95) 100%), url('{quest_bg_b64}'); background-size: cover;">
                <div>
                    <div class="studio-card-tag tag-sage">ATELIER II &bull; WORLD-BUILDING</div>
                    <div style="font-family: var(--font-display); font-size: 1.45rem; font-weight: 600; color: var(--text-ivory);">Quest Studio</div>
                    <div style="font-family: var(--font-serif); font-style: italic; font-size: 0.95rem; color: var(--accent-sage); margin-bottom: 0.6rem;">"Plan. Build. Adventure."</div>
                    <p style="color: var(--text-cream); font-size: 0.92rem; line-height: 1.5; font-family: var(--font-serif);">
                        Design structured RPG quests with objectives, difficulty balancing, NPC dialogues, rewards, and lore.
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Create Quest →", key="btn_card_quest", use_container_width=True):
            navigate_to("Quest Studio")

    # 3. Image Studio Card
    with c3:
        st.markdown(f"""
            <div class="studio-card" style="background-image: linear-gradient(180deg, rgba(37, 40, 32, 0.75) 0%, rgba(37, 40, 32, 0.95) 100%), url('{image_bg_b64}'); background-size: cover;">
                <div>
                    <div class="studio-card-tag tag-gold">ATELIER III &bull; VISUAL ARTS</div>
                    <div style="font-family: var(--font-display); font-size: 1.45rem; font-weight: 600; color: var(--text-ivory);">Image Studio</div>
                    <div style="font-family: var(--font-serif); font-style: italic; font-size: 0.95rem; color: var(--accent-gold); margin-bottom: 0.6rem;">"Imagine. Create. Visualize."</div>
                    <p style="color: var(--text-cream); font-size: 0.92rem; line-height: 1.5; font-family: var(--font-serif);">
                        Extract creative inspiration with Nemotron Vision, or synthesize classical illustrations with FLUX.
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Create Image →", key="btn_card_image", use_container_width=True):
            navigate_to("Image Studio")
