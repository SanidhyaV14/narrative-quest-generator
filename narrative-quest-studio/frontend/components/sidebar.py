"""
Narrative Studio — Persistent Sidebar Navigation Component
Adheres to the PART 8 Dark Academia specification.
"""

import streamlit as st
from frontend.components.navigation import navigate_to, init_navigation
from frontend.utils.session import is_authenticated, get_current_user, logout_user
from frontend.utils.assets import get_asset_base64 as get_image_base64


def render_sidebar():
    """Renders the Dark Academia branded sidebar navigation with history tracking."""
    init_navigation()

    with st.sidebar:
        # 1. Brand Header
        st.markdown("""
            <div style="padding: 0.8rem 0 1.2rem 0; border-bottom: 1px solid var(--border-color); margin-bottom: 1.2rem;">
                <div style="font-family: var(--font-display); font-size: 1.55rem; font-weight: 700; color: var(--accent-gold); letter-spacing: 0.08em; line-height: 1.1;">
                    NARRATIVE STUDIO
                </div>
                <div style="font-family: var(--font-sans); font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.16em; color: var(--accent-olive); margin-top: 0.35rem; font-weight: 700;">
                    A PRIVATE CREATIVE ARCHIVE
                </div>
                <div style="font-family: var(--font-reading); font-style: italic; font-size: 0.86rem; color: var(--parchment); margin-top: 0.35rem;">
                    "Where imagination meets atmosphere."
                </div>
            </div>
        """, unsafe_allow_html=True)

        current = st.session_state.get("current_page", "Dashboard")
        auth = is_authenticated()

        if auth:
            # 2. Main Navigation Section
            st.markdown("<p style='font-family: var(--font-sans); font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.14em; color: var(--accent-gold); margin-bottom: 0.4rem; font-weight: 700;'>NAVIGATION</p>", unsafe_allow_html=True)
            nav_items = [
                ("Dashboard", "Dashboard"),
                ("Story Generator", "Story Generator"),
                ("Quest Generator", "Quest Generator"),
                ("Image Studio", "Image Studio"),
                ("My Projects", "My Projects")
            ]

            for label, target in nav_items:
                is_active = (current == target)
                prefix = "✦ " if is_active else "  "
                btn_type = "primary" if is_active else "secondary"
                if st.button(f"{prefix}{label}", key=f"sidebar_nav_{target.lower().replace(' ', '_')}", use_container_width=True, type=btn_type):
                    navigate_to(target)

            st.markdown("<div style='border-bottom: 1px solid rgba(195, 167, 123, 0.2); margin: 1.4rem 0 1rem 0;'></div>", unsafe_allow_html=True)

            # 3. Preferences Section
            st.markdown("<p style='font-family: var(--font-sans); font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.14em; color: var(--text-muted); margin-bottom: 0.4rem; font-weight: 700;'>PREFERENCES</p>", unsafe_allow_html=True)
            is_settings = (current == "Settings")
            if st.button(f"{'✦ ' if is_settings else '  '}Settings", key="sidebar_nav_settings", use_container_width=True):
                navigate_to("Settings")

            st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)

            # 4. Account Bookplate & Identity
            user_info = get_current_user()
            st.markdown(f"""
                <div style="background-color: var(--bg-card); border: 1px solid rgba(195, 167, 123, 0.3); border-radius: 6px; padding: 0.8rem 0.9rem; margin-bottom: 0.8rem; box-shadow: inset 0 0 12px rgba(0, 0, 0, 0.45);">
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.25rem;">
                        <span style="font-family: var(--font-sans); font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.14em; color: var(--accent-gold); font-weight: 700;">
                            ⚜ Archival Fellow
                        </span>
                        <span style="font-family: var(--font-sans); font-size: 0.65rem; color: var(--accent-olive); font-weight: 700;">&bull; ACTIVE</span>
                    </div>
                    <div style="font-family: var(--font-display); font-weight: 600; color: var(--text-primary); font-size: 0.95rem; letter-spacing: 0.02em;">
                        {user_info['username']}
                    </div>
                    <div style="color: var(--text-muted); font-size: 0.76rem; font-family: var(--font-sans); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; margin-top: 0.1rem;">
                        {user_info['email']}
                    </div>
                </div>
            """, unsafe_allow_html=True)

            if st.button("Log Out of Atelier", key="sidebar_btn_logout", use_container_width=True):
                logout_user()
                st.rerun()

        else:
            # Unauthenticated Navigation
            st.markdown("<p style='font-family: var(--font-sans); font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.14em; color: var(--accent-gold); margin-bottom: 0.4rem; font-weight: 700;'>ARCHIVE ACCESS</p>", unsafe_allow_html=True)
            auth_items = ["Login", "Register"]
            for target in auth_items:
                is_active = (current == target)
                btn_type = "primary" if is_active else "secondary"
                if st.button(f"{'✦ ' if is_active else '  '}{target}", key=f"sidebar_auth_{target.lower()}", use_container_width=True, type=btn_type):
                    st.session_state["current_page"] = target
                    st.rerun()
