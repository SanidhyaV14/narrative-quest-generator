"""
Narrative Studio — Session State & Authentication State Manager
"""

import streamlit as st
from typing import Optional, Dict, Any


def init_session_state():
    """Initializes all necessary session-state variables if they do not exist."""
    if "token" not in st.session_state:
        st.session_state["token"] = None
    if "user" not in st.session_state:
        st.session_state["user"] = None
    if "nav_history" not in st.session_state:
        st.session_state["nav_history"] = []
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "Dashboard" if st.session_state.get("token") else "Login"
    if "selected_project_id" not in st.session_state:
        st.session_state["selected_project_id"] = None
    if "current_reference_image" not in st.session_state:
        st.session_state["current_reference_image"] = None


def is_authenticated() -> bool:
    """Returns True if a valid user token is present in session state."""
    return bool(st.session_state.get("token"))


def get_current_user() -> Dict[str, Any]:
    """Returns the authenticated user dict or dignified guest scholar details."""
    user = st.session_state.get("user") or {}
    raw_user = user.get("username", "")
    raw_email = user.get("email", "")
    username = "Archival Scholar" if not raw_user or "demo" in raw_user.lower() else raw_user
    email = "scholar@narrativestudio.ai" if not raw_email or "demo" in raw_email.lower() else raw_email
    return {
        "id": user.get("id"),
        "username": username,
        "email": email
    }


def login_user(user_data: Dict[str, Any], token: str):
    """Sets user credentials and routes to Dashboard."""
    st.session_state["token"] = token
    st.session_state["user"] = user_data
    st.session_state["current_page"] = "Dashboard"
    st.session_state["nav_history"] = []


def logout_user():
    """Clears authentication credentials and resets navigation to Login."""
    st.session_state["token"] = None
    st.session_state["user"] = None
    st.session_state["nav_history"] = []
    st.session_state["selected_project_id"] = None
    st.session_state["current_page"] = "Login"
