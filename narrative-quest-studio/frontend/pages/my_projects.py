"""
Narrative Studio — My Projects Collection
Adheres to PART 13: Premium Project Archive & Curated Catalog
"""

import streamlit as st
from frontend.config import BACKEND_URL
from frontend.components.navigation import render_back_button, navigate_to
from frontend.components.search import render_search_bar
from frontend.components.empty_states import render_empty_state
from frontend.utils.helpers import format_date, get_project_badge_html

try:
    from frontend.services.api_client import api_client
except (ModuleNotFoundError, ImportError):
    from services.api_client import api_client


def render_my_projects():
    """Renders the Dark Academia My Projects collection."""
    render_back_button(current_page="My Projects", section="Workspace")

    st.markdown("""
        <div style="margin-bottom: 1.5rem;">
            <div style="font-family: var(--font-sans); font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.16em; color: var(--accent-gold); font-weight: 700; margin-bottom: 0.3rem;">
                REPOSITORY &bull; PRIVATE ARCHIVE
            </div>
            <h1 style="margin: 0; color: var(--text-primary); font-family: var(--font-display); font-size: 2.3rem;">
                My Creative Collection
            </h1>
            <p style="font-family: var(--font-reading); font-style: italic; color: var(--parchment); font-size: 1.15rem; margin-top: 0.25rem;">
                "Every story, world, quest, and image you've created, gathered in one place."
            </p>
        </div>
    """, unsafe_allow_html=True)

    # 1. Filter, Sort, & View Controls
    ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([1.5, 1.2, 1])

    with ctrl_col1:
        filter_type = st.radio(
            "Filter Category",
            options=["ALL", "STORY", "GAME_QUEST"],
            horizontal=True,
            label_visibility="collapsed"
        )

    with ctrl_col2:
        sort_choice = st.selectbox(
            "Sort Order",
            options=["Newest First", "Oldest First", "Title (A–Z)"],
            index=0,
            label_visibility="collapsed"
        )

    with ctrl_col3:
        view_mode = st.radio(
            "View Mode",
            options=["List View", "Grid Cards"],
            horizontal=True,
            label_visibility="collapsed"
        )

    # 2. Fetch Projects from Backend
    try:
        req_filter = None if filter_type == "ALL" else filter_type
        all_projects = api_client.list_projects(project_type=req_filter)
    except Exception as e:
        st.error(f"Failed to fetch archive: {str(e)}")
        all_projects = []

    # 3. Apply Sorting
    if sort_choice == "Newest First":
        all_projects = sorted(all_projects, key=lambda p: p.get("created_at", ""), reverse=True)
    elif sort_choice == "Oldest First":
        all_projects = sorted(all_projects, key=lambda p: p.get("created_at", ""))
    elif sort_choice == "Title (A–Z)":
        all_projects = sorted(all_projects, key=lambda p: p.get("title", "").lower())

    # 4. Search Filter
    filtered_projects = render_search_bar(all_projects)

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # 5. Empty State
    if not filtered_projects:
        render_empty_state(
            title="No works found in this catalog section.",
            description="Compose your first narrative manuscript or quest blueprint to begin curating your private collection.",
            cta_label="Start Composing →",
            on_cta_click=lambda: navigate_to("Story Generator")
        )
        return

    # 6. Render Projects
    selected_id = st.session_state.get("selected_project_id")

    if view_mode == "Grid Cards":
        grid_cols = st.columns(3)
        for idx, p in enumerate(filtered_projects):
            p_id = p.get("id")
            p_type = p.get("project_type")
            p_title = p.get("title")
            p_date = format_date(p.get("created_at", ""))
            badge_html = get_project_badge_html(p_type)

            with grid_cols[idx % 3]:
                with st.container(border=True):
                    st.markdown(badge_html, unsafe_allow_html=True)
                    st.markdown(f"<h3 style='margin: 0.2rem 0; font-size: 1.25rem; color: var(--text-primary);'>{p_title}</h3>", unsafe_allow_html=True)
                    st.caption(f"{p_date} &bull; #{p_id}")

                    c_act1, c_act2 = st.columns(2)
                    with c_act1:
                        if st.button("Inspect →", key=f"grid_view_{p_id}", use_container_width=True):
                            st.session_state["selected_project_id"] = p_id
                            st.rerun()
                    with c_act2:
                        if st.button("Delete", key=f"grid_del_{p_id}", use_container_width=True):
                            st.session_state[f"confirm_delete_{p_id}"] = True

                    if st.session_state.get(f"confirm_delete_{p_id}"):
                        st.warning("Confirm permanent deletion?")
                        y_c1, y_c2 = st.columns(2)
                        with y_c1:
                            if st.button("Confirm", key=f"conf_y_{p_id}", type="primary", use_container_width=True):
                                try:
                                    api_client.delete_project(p_id)
                                    st.toast(f"Record #{p_id} excised from archive.")
                                    st.session_state[f"confirm_delete_{p_id}"] = False
                                    if selected_id == p_id:
                                        st.session_state["selected_project_id"] = None
                                    st.rerun()
                                except Exception as err:
                                    st.error(str(err))
                        with y_c2:
                            if st.button("Cancel", key=f"conf_n_{p_id}", use_container_width=True):
                                st.session_state[f"confirm_delete_{p_id}"] = False
                                st.rerun()

    else:
        # List View
        for p in filtered_projects:
            p_id = p.get("id")
            p_type = p.get("project_type")
            p_title = p.get("title")
            p_date = format_date(p.get("updated_at") or p.get("created_at", ""))
            badge_html = get_project_badge_html(p_type)

            with st.container(border=True):
                col1, col2, col3, col4 = st.columns([3.5, 1.3, 1.3, 1.1])
                with col1:
                    st.markdown(badge_html, unsafe_allow_html=True)
                    st.markdown(f"<h3 style='margin: 0.15rem 0; font-size: 1.35rem; color: var(--text-primary);'>{p_title}</h3>", unsafe_allow_html=True)
                    st.caption(f"Archived: {p_date} &bull; Catalog ID: #{p_id}")
                with col2:
                    st.write("")
                    view_clicked = st.button("Inspect Details", key=f"view_{p_id}", use_container_width=True)
                with col3:
                    st.write("")
                    export_text = api_client.export_project_txt(p_id) if (view_clicked or selected_id == p_id) else ""
                    if export_text:
                        st.download_button(
                            label="Export TXT 📥",
                            data=export_text,
                            file_name=f"{p_title.lower().replace(' ', '_')}_{p_id}.txt",
                            mime="text/plain",
                            key=f"dl_{p_id}",
                            use_container_width=True
                        )
                    else:
                        st.button("Export TXT", key=f"pre_exp_{p_id}", disabled=True, use_container_width=True)
                with col4:
                    st.write("")
                    if st.button("Delete", key=f"del_{p_id}", use_container_width=True):
                        st.session_state[f"confirm_del_list_{p_id}"] = True

                if st.session_state.get(f"confirm_del_list_{p_id}"):
                    st.warning(f"Confirm permanent deletion of #{p_id} '{p_title}'?")
                    d_c1, d_c2 = st.columns(2)
                    with d_c1:
                        if st.button("Confirm Deletion", key=f"cd_yes_{p_id}", type="primary", use_container_width=True):
                            try:
                                api_client.delete_project(p_id)
                                st.toast(f"Record #{p_id} removed.")
                                st.session_state[f"confirm_del_list_{p_id}"] = False
                                if selected_id == p_id:
                                    st.session_state["selected_project_id"] = None
                                st.rerun()
                            except Exception as err:
                                st.error(str(err))
                    with d_c2:
                        if st.button("Cancel", key=f"cd_no_{p_id}", use_container_width=True):
                            st.session_state[f"confirm_del_list_{p_id}"] = False
                            st.rerun()

                if view_clicked:
                    st.session_state["selected_project_id"] = p_id

    # 7. Expanded Project Inspection Panel
    active_project_id = st.session_state.get("selected_project_id")
    if active_project_id:
        active_p = next((proj for proj in all_projects if proj.get("id") == active_project_id), None)
        if active_p:
            st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
            with st.container(border=True):
                p_type = active_p.get("project_type")
                content = active_p.get("generated_content", {})

                st.markdown(f"""
                    <div style="border-bottom: 1px solid rgba(195, 167, 123, 0.25); padding-bottom: 0.8rem; margin-bottom: 1.2rem;">
                        <span class="badge-tag badge-gold">INSPECTING RECORD #{active_project_id}</span>
                        <h2 style="margin: 0.2rem 0; border: none; font-size: 1.85rem; color: var(--text-primary);">
                            {active_p.get('title')}
                        </h2>
                    </div>
                """, unsafe_allow_html=True)

                if p_type == "STORY":
                    st.markdown("<h4 style='color: var(--bronze); margin-top: 0;'>Prologue</h4>", unsafe_allow_html=True)
                    st.markdown(f"<div class='story-prose'>{content.get('introduction', '')}</div>", unsafe_allow_html=True)

                    st.markdown("<h4 style='color: var(--bronze); margin-top: 1.2rem;'>The Manuscript Arc</h4>", unsafe_allow_html=True)
                    st.markdown(f"<div class='story-prose'>{content.get('complete_story', 'No story manuscript text.')}</div>", unsafe_allow_html=True)

                    st.markdown("<h4 style='color: var(--bronze); margin-top: 1.2rem;'>Resolution</h4>", unsafe_allow_html=True)
                    st.markdown(f"<div class='story-prose'>{content.get('ending', '')}</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<h4 style='color: var(--accent-olive); margin-top: 0;'>Quest Log & Objectives</h4>", unsafe_allow_html=True)
                    st.markdown(f"<div class='story-prose'>{content.get('quest_description', '')}</div>", unsafe_allow_html=True)

                    st.markdown("<h5 style='margin-top: 1rem;'>Milestones & Stages</h5>", unsafe_allow_html=True)
                    st.write(content.get("objectives", ""))

                    st.markdown("<h5 style='margin-top: 1rem;'>Rewards</h5>", unsafe_allow_html=True)
                    st.write(content.get("rewards", ""))

                # Associated artwork
                images = active_p.get("images", [])
                if images:
                    st.markdown("<h4 style='color: var(--accent-gold); margin-top: 1.4rem;'>Associated Illustrations</h4>", unsafe_allow_html=True)
                    img_cols = st.columns(min(len(images), 3))
                    for idx, img in enumerate(images):
                        with img_cols[idx % 3]:
                            img_p = img.get("file_path") or img.get("image_path") or ""
                            st.image(f"{BACKEND_URL}/{img_p}", caption=f"[{img.get('image_type', 'ILLUSTRATION')}]", use_container_width=True)

                # Star Rating & Archival Critique
                st.markdown("<hr style='margin: 1.4rem 0; border-color: rgba(195, 167, 123, 0.2);'>", unsafe_allow_html=True)
                st.markdown("<div style='font-family: var(--font-sans); font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.12em; color: var(--accent-gold);'>Archival Rating & Critique</div>", unsafe_allow_html=True)
                fb_c1, fb_c2, fb_c3 = st.columns([1.2, 3, 1.2])
                with fb_c1:
                    rating = st.selectbox("Rating", options=[5, 4, 3, 2, 1], format_func=lambda x: f"{'★' * x} ({x}/5)", key=f"rate_{active_project_id}")
                with fb_c2:
                    comment = st.text_input("Reviewer Notes", placeholder="e.g. Compelling narrative arc and atmospheric tension", key=f"comment_{active_project_id}")
                with fb_c3:
                    st.write("")
                    if st.button("Submit Critique", key=f"sub_critique_{active_project_id}", use_container_width=True):
                        try:
                            api_client.submit_feedback(active_project_id, rating, comment)
                            st.toast("Critique recorded in project ledger!")
                        except Exception as err:
                            st.error(str(err))
