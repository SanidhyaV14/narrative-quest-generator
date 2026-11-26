"""
Narrative Studio — Main Streamlit Application Entrypoint
Dark Academia + Antique University Library + Luxury Editorial System
"""

import sys
from pathlib import Path

# Ensure project root and frontend directories are in sys.path
if "__file__" in globals():
    ROOT_DIR = Path(__file__).resolve().parent.parent
    FRONTEND_DIR = Path(__file__).resolve().parent
else:
    ROOT_DIR = Path.cwd().resolve()
    FRONTEND_DIR = ROOT_DIR / "frontend"

for p in (str(ROOT_DIR), str(FRONTEND_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

import streamlit as st
from frontend.utils.styles import FONT_IMPORTS_HTML, GLOBAL_CSS
from frontend.utils.session import init_session_state, is_authenticated
from frontend.components.navigation import init_navigation, render_top_navigation

# 1. Page Configuration
st.set_page_config(
    page_title="Narrative Studio — Private Creative Archive",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Inject Google Fonts & Global Dark Academia Stylesheet
st.markdown(FONT_IMPORTS_HTML, unsafe_allow_html=True)
st.markdown(f"<style>{GLOBAL_CSS}</style>", unsafe_allow_html=True)

# 3. Session State & Navigation Stack Initialization
init_session_state()
init_navigation()

# 4. Top Editorial Navigation (Sidebar Removed)
render_top_navigation()

# 5. Import Pages
from frontend.pages.dashboard import render_dashboard
from frontend.pages.story_generator import render_story_generator
from frontend.pages.quest_generator import render_quest_generator
from frontend.pages.image_studio import render_image_studio
from frontend.pages.my_projects import render_my_projects
from frontend.pages.login import render_login
from frontend.pages.register import render_register
from frontend.pages.settings import render_settings

# 6. Page Routing
authenticated = is_authenticated()
current_page = st.session_state.get("current_page", "Dashboard" if authenticated else "Login")

if authenticated:
    if current_page in ("Dashboard", "Overview"):
        render_dashboard()
    elif current_page in ("Story Generator", "Story Studio"):
        render_story_generator()
    elif current_page in ("Quest Generator", "Quest Studio"):
        render_quest_generator()
    elif current_page == "Image Studio":
        render_image_studio()
    elif current_page in ("My Projects", "Creative Archive"):
        render_my_projects()
    elif current_page == "Settings":
        render_settings()
    else:
        render_dashboard()
else:
    if current_page in ("Register", "Create Account"):
        render_register()
    else:
        render_login()
