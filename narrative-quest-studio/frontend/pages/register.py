"""
Narrative Studio — Register Page
Adheres to PART 14: Dark Translucent Authentication Screen
"""

import streamlit as st
from frontend.utils.assets import get_asset_base64
from frontend.utils.session import login_user

try:
    from frontend.services.api_client import api_client
except (ModuleNotFoundError, ImportError):
    from services.api_client import api_client


def render_register():
    """Renders the Dark Academia editorial split-layout registration experience."""
    auth_b64 = get_asset_base64("auth_bg.png")

    col_art, col_form = st.columns([1.2, 1])

    with col_art:
        st.markdown(f"""
            <div style="background-image: linear-gradient(180deg, rgba(17, 19, 15, 0.45) 0%, rgba(17, 19, 15, 0.95) 100%), url('{auth_b64}'); background-size: cover; background-position: center; border-radius: 8px; border: 1px solid var(--border-color); padding: 3.5rem 2.5rem; min-height: 520px; display: flex; flex-direction: column; justify-content: flex-end; box-shadow: 0 8px 30px rgba(0, 0, 0, 0.6);">
                <div style="font-family: var(--font-sans); font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.16em; color: var(--accent-gold); font-weight: 700; margin-bottom: 0.4rem;">
                    NARRATIVE STUDIO &bull; INITIATION
                </div>
                <div style="font-family: var(--font-display); font-size: 2.2rem; font-weight: 700; color: var(--text-primary); line-height: 1.15; margin-bottom: 0.6rem;">
                    "Begin your creative journey."
                </div>
                <p style="color: var(--parchment); font-size: 0.96rem; line-height: 1.6; margin: 0; font-family: var(--font-reading);">
                    Join our literary atelier to compose memorable narratives, design interactive worlds, and store your creative lore.
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col_form:
        with st.container(border=True):
            st.markdown("""
                <div style="margin-bottom: 1.2rem;">
                    <div style="font-family: var(--font-sans); font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.12em; color: var(--accent-gold); font-weight: 700;">MEMBERSHIP</div>
                    <h2 style="border: none; margin: 0.2rem 0; font-size: 1.9rem; color: var(--text-primary); font-family: var(--font-display);">Create Account</h2>
                    <p style="color: var(--text-muted); font-size: 0.9rem; margin: 0; font-family: var(--font-sans);">Establish your personal archive ledger.</p>
                </div>
            """, unsafe_allow_html=True)

            username = st.text_input("Author Pseudonym / Username", placeholder="e.g. ArcaneScholar")
            email = st.text_input("Email Address", placeholder="scholar@domain.com")
            password = st.text_input("Password", type="password", help="Minimum 6 characters")
            confirm_password = st.text_input("Confirm Password", type="password")

            if st.button("Establish Account →", type="primary", use_container_width=True):
                if not username or not email or not password:
                    st.error("Please complete all required fields.")
                elif password != confirm_password:
                    st.error("Passwords do not match.")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters long.")
                else:
                    with st.spinner("Recording new author in registry..."):
                        try:
                            res = api_client.register(
                                username=username.strip(),
                                email=email.strip(),
                                password=password,
                                confirm_password=confirm_password
                            )
                            login_user(res["user"], res["access_token"])
                            st.rerun()
                        except Exception as e:
                            st.error(str(e))

            st.markdown("<hr style='margin: 1.2rem 0; border-color: rgba(195, 167, 123, 0.2);'>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: var(--text-muted); font-size: 0.85rem; font-family: var(--font-sans);'>Already an archived author?</p>", unsafe_allow_html=True)
            if st.button("Sign In to Existing Archive", use_container_width=True):
                st.session_state["current_page"] = "Login"
                st.rerun()
