import streamlit as st
from frontend.utils.assets import get_asset_base64 as get_image_base64


def render_hero():
    """Renders the cinematic grand library hero banner."""
    hero_img_b64 = get_image_base64("assets/images/grand_library_hero.png")
    bg_style = f"background-image: url('{hero_img_b64}');" if hero_img_b64 else "background-color: var(--surface-primary);"

    st.markdown(f"""
        <div class="editorial-hero" style="{bg_style}">
            <div class="editorial-hero-content">
                <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.15em; color: var(--accent-gold); font-weight: 600; margin-bottom: 0.5rem;">
                    LITERARY ATELIER & ARCHIVE
                </div>
                <h1>Welcome to your creative archive.</h1>
                <p>
                    A place for stories yet to be written, worlds waiting to be discovered, and ideas worth preserving.
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("Start Creating →", key="btn_hero_cta", type="primary", use_container_width=True):
            st.session_state["current_page"] = "Story Studio"
            st.rerun()
