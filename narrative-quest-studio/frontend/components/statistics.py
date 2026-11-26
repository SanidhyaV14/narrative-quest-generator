"""
Narrative Studio — Statistics Component
Renders 3 compact, elegant archive metrics.
"""

import streamlit as st


def render_archive_statistics(total_projects: int, story_count: int, quest_count: int):
    """Renders 3 compact statistics metrics with Dark Academia styling."""
    with st.container(border=True):
        st.markdown("""
            <div style="font-family: var(--font-sans); font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.14em; color: var(--accent-gold); font-weight: 700; margin-bottom: 0.6rem;">
                ARCHIVE CATALOG OVERVIEW
            </div>
        """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Saved Projects", total_projects)
        with col2:
            st.metric("Stories Created", story_count)
        with col3:
            st.metric("Quests Designed", quest_count)
