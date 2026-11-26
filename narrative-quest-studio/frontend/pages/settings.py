"""
Narrative Studio — Settings & Preferences Page
Adheres to PART 15: Minimal Settings Environment
"""

import streamlit as st
import requests
from frontend.config import BACKEND_URL
from frontend.components.navigation import render_back_button, navigate_to
from frontend.utils.session import get_current_user


def render_settings():
    """Renders the Dark Academia Settings and Preferences page."""
    render_back_button(current_page="Settings", section="Preferences")

    st.markdown("""
        <div style="margin-bottom: 2rem;">
            <div style="font-family: var(--font-sans); font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.16em; color: var(--accent-gold); font-weight: 700; margin-bottom: 0.3rem;">
                WORKSPACE &bull; PREFERENCES
            </div>
            <h1 style="margin: 0; color: var(--text-primary); font-family: var(--font-display); font-size: 2.3rem;">
                Settings & Preferences
            </h1>
            <p style="font-family: var(--font-reading); font-style: italic; color: var(--parchment); font-size: 1.15rem; margin-top: 0.25rem;">
                "Configure your reading atmosphere, archival membership, and gateway connectivity."
            </p>
        </div>
    """, unsafe_allow_html=True)

    tab_appearance, tab_account, tab_diag = st.tabs([
        "Appearance & Typography",
        "Archival Membership",
        "System Connectivity"
    ])

    # 1. Appearance & Typography
    with tab_appearance:
        with st.container(border=True):
            st.markdown("<h3 style='margin-top: 0;'>Atelier Aesthetic Environment</h3>", unsafe_allow_html=True)
            st.caption("Customize your Dark Academia reading and composition environment.")

            theme_choice = st.radio(
                "Visual Environment Theme",
                options=["Dark Academia (Classic Oxford)", "Antique Parchment & Leather", "Midnight Obsidian"],
                index=0
            )
            st.checkbox("Enable Atmospheric Grain & Subtle Motion", value=True)
            st.checkbox("High-Legibility Serif Reading Prose (Lora / Cormorant)", value=True)

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown("<h3 style='margin-top: 0;'>Manuscript Typography Scale</h3>", unsafe_allow_html=True)
            st.caption("Adjust typographic scale for long-form reading and editing comfort.")
            st.select_slider(
                "Manuscript Reading Sizing",
                options=["Compact Folio (14px)", "Standard Octavo (16px)", "Scholarly Quarto (18px)", "Grand Imperial (20px)"],
                value="Scholarly Quarto (18px)"
            )

    # 2. Archival Membership & Profile
    with tab_account:
        with st.container(border=True):
            st.markdown("<h3 style='margin-top: 0;'>Author Registry Bookplate</h3>", unsafe_allow_html=True)
            user_info = get_current_user()

            col_u1, col_u2 = st.columns(2)
            with col_u1:
                st.markdown(f"**Archived Pseudonym:** `{user_info['username']}`")
                st.markdown(f"**Registered Registry:** `{user_info['email']}`")
            with col_u2:
                st.markdown("**Membership Rank:** `Fellow of the Narrative Atelier`")
                st.markdown("**Archival Vault Status:** `Active (Encrypted Local Storage)`")

            st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)
            if st.button("Browse My Creative Collection →", use_container_width=True):
                navigate_to("My Projects")

    # 3. System Connectivity & Gateway Probe
    with tab_diag:
        with st.container(border=True):
            st.markdown("<h3 style='margin-top: 0;'>Creative Gateway Connectivity</h3>", unsafe_allow_html=True)
            st.caption(f"Inspecting live connection to the Narrative Studio API server at `{BACKEND_URL}`.")

            if st.button("Probe Gateway Health ⚡", key="btn_probe_health"):
                with st.spinner("Pinging API gateway..."):
                    try:
                        resp = requests.get(f"{BACKEND_URL}/api/health", timeout=3)
                        if resp.ok:
                            st.success(f"Creative Gateway Status: ONLINE &bull; {resp.json().get('service', 'Operational')}")
                        else:
                            st.warning(f"Gateway responded with status code HTTP {resp.status_code}")
                    except Exception as e:
                        st.error(f"Could not reach gateway: {str(e)}")

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown("<h3 style='margin-top: 0;'>Application Information</h3>", unsafe_allow_html=True)
            st.markdown("""
                - **Application:** Narrative Studio — Multimodal AI Creative Atelier
                - **Platform:** Streamlit & FastAPI
                - **AI Engines:** NVIDIA Nemotron & FLUX.1-dev
                - **Version:** 2.0 (Dark Academia Edition)
            """)
