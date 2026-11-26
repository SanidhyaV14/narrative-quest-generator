"""
Narrative Studio — Empty State Component
Renders an elegant Dark Academia empty state with clean illustration display.
"""

import streamlit as st
from frontend.utils.assets import get_asset_path, asset_exists


def render_empty_state(
    title: str = "No records found in this archive section.",
    description: str = "Your creative journey begins with a single idea. Enter one of the creative studios to compose your first work.",
    cta_label: str = "Begin Creation →",
    on_cta_click=None
):
    """
    Renders an elegant Dark Academia empty state.
    Uses native image display for decorative_illustrations.png to guarantee
    no markdown parser or code block escaping issues.
    """
    with st.container(border=True):
        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

        # Centered decorative illustration accent
        if asset_exists("decorative_illustrations.png"):
            col_l, col_img, col_r = st.columns([1.5, 1.2, 1.5])
            with col_img:
                st.image(str(get_asset_path("decorative_illustrations.png")), use_container_width=True)
        else:
            st.markdown(
                "<div style='text-align: center; color: var(--accent-gold); font-size: 1.5rem; letter-spacing: 0.3em; margin: 0.8rem 0;'>✦ &nbsp; ⚜ &nbsp; ✦</div>",
                unsafe_allow_html=True
            )

        # Title and description with zero-indent HTML to prevent markdown code block parsing
        body_html = (
            f"<div style='text-align: center; margin: 0.8rem 0 1.4rem 0;'>"
            f"<div style=\"font-family: var(--font-display); font-size: 1.5rem; color: var(--text-primary); margin-bottom: 0.4rem; font-weight: 600;\">{title}</div>"
            f"<p style=\"color: var(--parchment); max-width: 520px; margin: 0 auto; font-size: 0.98rem; font-family: var(--font-reading); line-height: 1.6;\">{description}</p>"
            f"</div>"
        )
        st.markdown(body_html, unsafe_allow_html=True)

        if cta_label and on_cta_click:
            c1, c2, c3 = st.columns([1.3, 1, 1.3])
            with c2:
                if st.button(cta_label, type="primary", use_container_width=True):
                    on_cta_click()

        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
