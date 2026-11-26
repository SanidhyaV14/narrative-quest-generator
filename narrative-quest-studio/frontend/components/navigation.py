"""
Narrative Studio — Navigation Controller & Header Navigation
Replaces the sidebar with an editorial Dark Academia top navigation bar.
"""

import streamlit as st
from frontend.utils.session import is_authenticated, get_current_user, logout_user


def init_navigation():
    """Initializes navigation state and history stack if not present."""
    if "nav_history" not in st.session_state:
        st.session_state["nav_history"] = []
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "Dashboard" if st.session_state.get("token") else "Login"


def navigate_to(target_page: str):
    """
    Navigates to the target page, pushing the current page onto the navigation history stack.
    Avoids duplicate consecutive entries.
    """
    init_navigation()
    current = st.session_state.get("current_page", "Dashboard")
    if current != target_page:
        history = st.session_state.get("nav_history", [])
        if not history or history[-1] != current:
            history.append(current)
            if len(history) > 20:
                history.pop(0)
            st.session_state["nav_history"] = history
        st.session_state["current_page"] = target_page
        st.rerun()


def go_back(fallback: str = "Dashboard"):
    """
    Pops the most recent page from navigation history and navigates back to it.
    If history is empty or equals the current page, navigates to the fallback page.
    """
    init_navigation()
    history = st.session_state.get("nav_history", [])
    current = st.session_state.get("current_page", "Dashboard")

    while history and history[-1] == current:
        history.pop()

    if history:
        prev_page = history.pop()
        st.session_state["nav_history"] = history
        st.session_state["current_page"] = prev_page
    else:
        st.session_state["current_page"] = fallback
    
    st.rerun()


def render_top_navigation():
    """
    Renders the persistent editorial Dark Academia top navigation bar.
    Contains:
    - Atelier brand identity and subtitle
    - User account badge and logout action (or Sign In / Register when logged out)
    - 6-tab horizontal navigation pills
    - Fine gold separator
    """
    init_navigation()
    current = st.session_state.get("current_page", "Dashboard")
    auth = is_authenticated()

    # Row 1: Brand Context & User Bookplate
    col_brand, col_user = st.columns([2.4, 1.4])

    with col_brand:
        st.markdown("""
            <div style="display: flex; align-items: baseline; gap: 0.8rem; padding: 0.2rem 0;">
                <span style="font-family: var(--font-display); font-size: 1.65rem; font-weight: 700; color: var(--accent-gold); letter-spacing: 0.08em; text-shadow: 0 2px 8px rgba(0,0,0,0.6);">
                    NARRATIVE STUDIO
                </span>
                <span style="font-family: var(--font-sans); font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.16em; color: var(--accent-olive); font-weight: 700;">
                    A PRIVATE CREATIVE ARCHIVE
                </span>
            </div>
        """, unsafe_allow_html=True)

    with col_user:
        if auth:
            user_info = get_current_user()
            u_c1, u_c2 = st.columns([2, 1.2])
            with u_c1:
                st.markdown(f"""
                    <div style="text-align: right; padding-top: 0.25rem;">
                        <span style="font-family: var(--font-sans); font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.12em; color: var(--accent-gold); font-weight: 700;">
                            ⚜ Archival Fellow
                        </span>
                        <div style="font-family: var(--font-display); font-size: 0.95rem; color: var(--text-primary); font-weight: 600; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                            {user_info['username']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            with u_c2:
                st.write("")
                if st.button("Log Out", key="top_nav_logout", use_container_width=True):
                    logout_user()
                    st.rerun()
        else:
            a_c1, a_c2 = st.columns(2)
            with a_c1:
                if st.button("Sign In", key="top_nav_signin", use_container_width=True, type="primary" if current == "Login" else "secondary"):
                    st.session_state["current_page"] = "Login"
                    st.rerun()
            with a_c2:
                if st.button("Register", key="top_nav_register", use_container_width=True, type="primary" if current == "Register" else "secondary"):
                    st.session_state["current_page"] = "Register"
                    st.rerun()

    # Row 2: Navigation Links (When Authenticated)
    if auth:
        nav_cols = st.columns(6)
        nav_items = [
            ("Dashboard", "Dashboard"),
            ("Story Generator", "Story Generator"),
            ("Quest Generator", "Quest Generator"),
            ("Image Studio", "Image Studio"),
            ("My Projects", "My Projects"),
            ("Settings", "Settings")
        ]
        for idx, (label, target) in enumerate(nav_items):
            with nav_cols[idx]:
                is_active = (current == target or (target == "Dashboard" and current == "Overview"))
                btn_type = "primary" if is_active else "secondary"
                prefix = "✦ " if is_active else ""
                if st.button(f"{prefix}{label}", key=f"top_nav_btn_{target.lower().replace(' ', '_')}", use_container_width=True, type=btn_type):
                    navigate_to(target)

    st.markdown("""
        <div style="border-bottom: 1px solid rgba(195, 167, 123, 0.22); margin-top: 0.5rem; margin-bottom: 1.4rem;"></div>
    """, unsafe_allow_html=True)


def render_back_button(current_page: str, section: str = "Creative Studios", fallback: str = "Dashboard"):
    """
    Renders an elegant Dark Academia back bar containing:
    - Dedicated '← Back' button returning to the previous page
    - Classical breadcrumb trail
    - Quick '🏛 Dashboard' jump button
    - Subtle antique gold hairline separator
    """
    init_navigation()
    key_slug = current_page.lower().replace(" ", "_").replace("&", "and")

    st.markdown("""
        <div style="margin-top: -0.6rem; margin-bottom: 0.4rem;"></div>
    """, unsafe_allow_html=True)

    col_back, col_crumbs, col_home = st.columns([1.3, 6.2, 1.5])

    with col_back:
        if st.button("← Back", key=f"nav_back_{key_slug}", help="Return to the previously viewed page", use_container_width=True):
            go_back(fallback=fallback)

    with col_crumbs:
        st.markdown(f"""
            <div style="display: flex; align-items: center; height: 100%; padding-left: 0.5rem;">
                <span class="breadcrumb-trail" style="font-family: var(--font-sans); font-size: 0.76rem; letter-spacing: 0.12em; color: var(--text-muted); text-transform: uppercase;">
                    {section} &nbsp;&bull;&nbsp; <span style="color: var(--accent-gold); font-weight: 600;">{current_page}</span>
                </span>
            </div>
        """, unsafe_allow_html=True)

    with col_home:
        if st.button("🏛 Dashboard", key=f"nav_dash_{key_slug}", help="Return directly to the central Dashboard", use_container_width=True):
            navigate_to("Dashboard")

    st.markdown("""
        <div style="border-bottom: 1px solid rgba(195, 167, 123, 0.2); margin-top: 0.5rem; margin-bottom: 1.2rem;"></div>
    """, unsafe_allow_html=True)
