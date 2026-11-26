"""
Narrative Studio — Page Header Component
"""

import streamlit as st
from frontend.utils.assets import get_hero_bg_style


def render_page_header(
    badge: str,
    title: str,
    subtitle: str,
    bg_asset: str = "",
    overlay_darkness: float = 0.85
):
    """
    Renders an editorial Dark Academia hero banner with an optional local asset background.
    """
    bg_style = get_hero_bg_style(bg_asset, overlay_darkness=overlay_darkness) if bg_asset else "background-color: var(--bg-card); border: 1px solid var(--border-color);"

    st.markdown(f"""
        <div style="{bg_style} border-radius: 8px; padding: 2.2rem 2.4rem; margin-bottom: 1.8rem; border: 1px solid var(--border-color); box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);">
            <div style="font-family: var(--font-sans); font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.16em; color: var(--accent-gold); font-weight: 700; margin-bottom: 0.35rem;">
                {badge}
            </div>
            <h1 style="margin: 0; color: var(--text-primary); font-family: var(--font-display); font-size: 2.35rem; font-weight: 700;">
                {title}
            </h1>
            <p style="font-family: var(--font-reading); font-style: italic; color: var(--parchment); font-size: 1.15rem; margin-top: 0.35rem; margin-bottom: 0; line-height: 1.5;">
                "{subtitle}"
            </p>
        </div>
    """, unsafe_allow_html=True)
