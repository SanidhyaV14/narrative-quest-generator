"""
Narrative Studio — Story Generator Page
Adheres to PART 10: Literary Writing Environment & Manuscript Studio
"""

import streamlit as st
from frontend.config import GENRES, THEMES, TONES, LENGTHS, BACKEND_URL
from frontend.components.navigation import render_back_button, navigate_to
from frontend.components.page_header import render_page_header
from frontend.utils.assets import get_asset_base64

try:
    from frontend.services.api_client import api_client
except (ModuleNotFoundError, ImportError):
    from services.api_client import api_client

WRITING_STYLES = [
    "Classical Gothic",
    "Atmospheric Dark Academia",
    "Epic High Fantasy",
    "Victorian Mystery",
    "Mythic Folklore",
    "Philosophical Fiction",
    "Grimdark Realism"
]

PERSPECTIVES = [
    "Third Person Limited",
    "Third Person Omniscient",
    "First Person (Protagonist)",
    "Epistolary (Letters & Journal Entries)"
]


def render_story_generator():
    """Renders the Dark Academia Story Generator writing atelier."""
    render_back_button(current_page="Story Generator", section="Creative Studios")

    render_page_header(
        badge="ATELIER I &bull; LITERARY CREATION",
        title="Story Generator",
        subtitle="Every great world begins with a story.",
        bg_asset="story_bg.png",
        overlay_darkness=0.88
    )

    # Pre-fill seed idea from Image Studio if present
    initial_idea = st.session_state.pop("story_seed_idea", "")
    ref_image_path = st.session_state.get("current_reference_image")

    # =========================================================================
    # INPUT SECTIONS (Organized into Elegant Expandable Panels)
    # =========================================================================
    with st.expander("📜 Section 1: Story Details & Framing", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            story_title = st.text_input("Story Title (Optional)", placeholder="e.g. The Chronicle of Aethelgard")
            genre = st.selectbox("Narrative Genre", options=GENRES, index=0)
            writing_style = st.selectbox("Writing Style", options=WRITING_STYLES, index=1)
        with col2:
            narrative_perspective = st.selectbox("Narrative Perspective", options=PERSPECTIVES, index=0)
            story_length = st.radio("Manuscript Scope", options=LENGTHS, index=1, horizontal=True)

    with st.expander("👤 Section 2: Characters & Relationships", expanded=False):
        c_col1, c_col2 = st.columns(2)
        with c_col1:
            main_character = st.text_input(
                "Protagonist & Motivation",
                value="Kaelen, a renegade archivist seeking forbidden celestial codices"
            )
            supporting_characters = st.text_input(
                "Supporting Characters (Optional)",
                placeholder="e.g. Master Elowen, a blind scholar of the High Vault"
            )
        with c_col2:
            character_relationships = st.text_input(
                "Character Dynamics / Alliances",
                placeholder="e.g. Bound by an oath to an antique order of astronomers"
            )
            character_descriptions = st.text_area(
                "Key Traits & Visual Notes",
                placeholder="e.g. Wears silver-rimmed spectacles and ink-stained velvet",
                height=70
            )

    with st.expander("🏛️ Section 3: World & Setting", expanded=False):
        w_col1, w_col2 = st.columns(2)
        with w_col1:
            setting = st.text_input(
                "Primary Location / World",
                value="The grand crystalline library spires of Aethelgard"
            )
            time_period = st.text_input(
                "Era / Time Period",
                placeholder="e.g. The Twilight of the Third Lunar Epoch"
            )
        with w_col2:
            world_building = st.text_input(
                "World-building Directives",
                placeholder="e.g. Astrology dictates the tides of magical power"
            )
            environment = st.text_input(
                "Atmospheric Environment",
                value="Perpetual midnight rain, candlelight flickering against towering mahogany shelves"
            )

    with st.expander("🖋️ Section 4: Narrative Conflict & Core Premise", expanded=True):
        n_col1, n_col2 = st.columns(2)
        with n_col1:
            theme = st.selectbox("Underlying Theme", options=THEMES, index=0)
            tone = st.selectbox("Literary Tone", options=TONES, index=3)
        with n_col2:
            conflict = st.text_input(
                "Core Conflict",
                value="The Grand Inquisitor has ordered the burning of all lunar star charts"
            )
            additional_instructions = st.text_input(
                "Stylistic & Lore Directives (Optional)",
                placeholder="e.g. Include sensory descriptions of parchment, dust, and ink"
            )

        story_idea = st.text_area(
            "Premise / Core Narrative Arc",
            value=initial_idea or "Kaelen infiltrates the deepest subterranean vault to rescue the Astrolabe of the Night Sun before the solstice.",
            height=100
        )

        st.markdown("<h5 style='margin-top: 0.8rem; color: var(--accent-gold);'>🖼️ Visual Reference (Optional)</h5>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Upload reference illustration (JPG, PNG — Max 5 MB)",
            type=["jpg", "jpeg", "png"],
            key="story_ref_file"
        )
        if uploaded_file:
            st.session_state["story_ref_file"] = uploaded_file
            st.caption(f"Loaded: {uploaded_file.name} ({uploaded_file.size / 1024:.1f} KB)")
        elif ref_image_path:
            st.caption(f"Using reference image from Image Studio: `{ref_image_path}`")

    # =========================================================================
    # GENERATION ACTION
    # =========================================================================
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    if st.button("Generate Complete Story Manuscript →", type="primary", use_container_width=True):
        if not story_idea:
            st.error("Please provide a story premise or narrative idea.")
        else:
            with st.spinner("NVIDIA Nemotron is composing your literary manuscript..."):
                try:
                    active_ref = ref_image_path
                    if uploaded_file:
                        up_res = api_client.upload_image(uploaded_file, "reference")
                        active_ref = up_res.get("file_path")

                    combined_instructions = f"Writing Style: {writing_style}. Perspective: {narrative_perspective}."
                    if conflict:
                        combined_instructions += f" Central Conflict: {conflict}."
                    if additional_instructions:
                        combined_instructions += f" {additional_instructions}"

                    payload = {
                        "title": story_title or f"The Chronicle of {setting[:25]}",
                        "genre": genre,
                        "theme": theme,
                        "tone": tone,
                        "setting": setting,
                        "main_character": main_character,
                        "story_length": story_length,
                        "story_idea": story_idea,
                        "additional_instructions": combined_instructions,
                        "reference_image_path": active_ref
                    }
                    res = api_client.generate_story(payload)
                    st.session_state["generated_story_data"] = res
                    st.toast("Manuscript successfully inscribed in memory!")
                except Exception as e:
                    st.error(f"Story generation failed: {str(e)}")

    # =========================================================================
    # GENERATED MANUSCRIPT PRESENTATION
    # =========================================================================
    story_data = st.session_state.get("generated_story_data")
    if story_data:
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        # Handle both direct API response {"data": {...}} and saved project record {"generated_content": {...}}
        content = story_data.get("data") or story_data.get("generated_content") or story_data
        title_disp = content.get("title") or story_data.get("title") or "Untitled Manuscript"

        with st.container(border=True):
            st.markdown(f"""
                <div style="border-bottom: 1px solid rgba(195, 167, 123, 0.25); padding-bottom: 1rem; margin-bottom: 1.5rem;">
                    <div style="font-family: var(--font-sans); font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.16em; color: var(--bronze); font-weight: 700;">
                        MANUSCRIPT ARCHIVE RECORD
                    </div>
                    <h1 style="font-family: var(--font-display); font-size: 2.2rem; color: var(--text-primary); margin: 0.2rem 0;">
                        {title_disp}
                    </h1>
                    <div style="font-family: var(--font-sans); font-size: 0.85rem; color: var(--text-muted);">
                        Genre: <span style="color: var(--accent-gold);">{content.get('genre', genre)}</span> &bull;
                        Theme: <span style="color: var(--parchment);">{content.get('theme', theme)}</span> &bull;
                        Setting: <span style="color: var(--parchment);">{content.get('setting', setting)}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            tab_read, tab_chapters, tab_art = st.tabs(["Complete Manuscript", "Chapter Codex", "Synthesize Illustration"])

            with tab_read:
                st.markdown("<h3 style='margin-top: 0;'>Prologue & Exposition</h3>", unsafe_allow_html=True)
                st.markdown(f"<div class='story-prose'>{content.get('introduction', '')}</div>", unsafe_allow_html=True)

                st.markdown("<h3 style='margin-top: 1.4rem;'>The Narrative Arc</h3>", unsafe_allow_html=True)
                complete_text = content.get('complete_story', '')
                st.markdown(f"<div class='story-prose'>{complete_text}</div>", unsafe_allow_html=True)

                st.markdown("<h3 style='margin-top: 1.4rem;'>Epilogue & Resolution</h3>", unsafe_allow_html=True)
                st.markdown(f"<div class='story-prose'>{content.get('ending', '')}</div>", unsafe_allow_html=True)

                # Copy / Download Plaintext
                full_export = f"{title_disp}\n{'=' * len(title_disp)}\n\nPROLOGUE:\n{content.get('introduction', '')}\n\nSTORY:\n{complete_text}\n\nEPILOGUE:\n{content.get('ending', '')}"
                st.download_button(
                    label="Download Manuscript (TXT) 📥",
                    data=full_export,
                    file_name=f"{title_disp.lower().replace(' ', '_')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )

            with tab_chapters:
                st.markdown("<h3 style='margin-top: 0;'>Characters & Motivations</h3>", unsafe_allow_html=True)
                chars_text = content.get("main_characters") or content.get("characters", "Not recorded.")
                st.markdown(f"<div class='story-prose'>{chars_text}</div>", unsafe_allow_html=True)

                st.markdown("<h3 style='margin-top: 1.4rem;'>World & Environmental Setting</h3>", unsafe_allow_html=True)
                setting_text = content.get("setting") or content.get("setting_details", "Not recorded.")
                st.markdown(f"<div class='story-prose'>{setting_text}</div>", unsafe_allow_html=True)

                st.markdown("<h3 style='margin-top: 1.4rem;'>Primary Conflict & Arc</h3>", unsafe_allow_html=True)
                conflict_text = content.get("conflict") or content.get("plot_outline", "Not recorded.")
                st.markdown(f"<div class='story-prose'>{conflict_text}</div>", unsafe_allow_html=True)

            with tab_art:
                st.markdown("<h3>Synthesize Story Illustration (FLUX.1-dev)</h3>", unsafe_allow_html=True)
                st.caption("Generate an illustration based on this story's atmosphere.")
                suggested_prompt = (
                    content.get("suggested_image_description")
                    or content.get("suggested_illustration_description")
                    or f"A classical oil painting representing {content.get('setting', setting)}, dramatic chiaroscuro lighting, dark academia aesthetic"
                )
                art_prompt = st.text_area("Artwork Prompt", value=suggested_prompt, height=85)
                art_style = st.selectbox("Visual Art Style", options=["Dark Academia", "Classical Oil Painting", "Dramatic Fantasy", "Vintage Etching"], index=0)

                if st.button("Synthesize Story Artwork →", type="primary", use_container_width=True):
                    with st.spinner("FLUX is painting your illustration..."):
                        try:
                            img_res = api_client.generate_image({
                                "prompt": art_prompt,
                                "art_style": art_style,
                                "mood": "Atmospheric",
                                "project_id": story_data.get("project_id")
                            })
                            st.session_state["story_illustration"] = img_res
                            st.toast("Illustration synthesized and cataloged!")
                        except Exception as e:
                            st.error(f"Illustration generation failed: {str(e)}")

                story_img = st.session_state.get("story_illustration")
                if story_img:
                    s_img_path = story_img.get("file_path") or story_img.get("image_path") or ""
                    st.image(f"{BACKEND_URL}/{s_img_path}", caption=f"FLUX Illustration: {art_style}", use_container_width=True)

            # Save / Export Actions
            st.markdown("<hr style='margin: 1.5rem 0; border-color: rgba(195, 167, 123, 0.2);'>", unsafe_allow_html=True)
            col_save1, col_save2 = st.columns([1, 1])
            with col_save1:
                if st.button("Save to My Projects Collection 💾", type="primary", use_container_width=True):
                    with st.spinner("Cataloging in permanent archive..."):
                        try:
                            saved = api_client.save_project({
                                "title": title_disp,
                                "project_type": "STORY",
                                "generated_content": content,
                                "reference_image_path": story_data.get("reference_image_path")
                            })
                            st.session_state["selected_project_id"] = saved.get("id")
                            st.toast("Project archived successfully!")
                            navigate_to("My Projects")
                        except Exception as e:
                            st.error(f"Failed to save project: {str(e)}")
            with col_save2:
                if st.button("Regenerate Story Arc ↻", use_container_width=True):
                    st.session_state["generated_story_data"] = None
                    st.rerun()
