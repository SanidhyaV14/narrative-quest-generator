"""
Narrative Studio — Quest Generator Page
Adheres to PART 11: Fantasy-Inspired Campaign Creation Environment
"""

import streamlit as st
from frontend.config import GAME_GENRES, QUEST_THEMES, DIFFICULTIES, ENDING_PREFERENCES, BACKEND_URL
from frontend.components.navigation import render_back_button, navigate_to
from frontend.components.page_header import render_page_header
from frontend.utils.assets import get_asset_base64

try:
    from frontend.services.api_client import api_client
except (ModuleNotFoundError, ImportError):
    from services.api_client import api_client

QUEST_TYPES = ["Main Quest", "Side Quest", "Exploration", "Mystery & Investigation", "Tactical Combat", "Ancient Puzzle"]
EXTENDED_DIFFICULTIES = ["Apprentice (Easy)", "Adventurer (Medium)", "Veteran (Hard)", "Mythic Legendary"]


def render_quest_generator():
    """Renders the Dark Academia Quest Generator world-building atelier."""
    render_back_button(current_page="Quest Generator", section="Creative Studios")

    render_page_header(
        badge="ATELIER II &bull; WORLD-BUILDING & RPG LORE",
        title="Quest Generator",
        subtitle="Build worlds. Design adventures. Create legends.",
        bg_asset="quest_bg.png",
        overlay_darkness=0.88
    )

    initial_idea = st.session_state.pop("quest_seed_idea", "")
    ref_image_path = st.session_state.get("current_reference_image")

    # =========================================================================
    # INPUT FIELDS (Organized into Campaign Codex Panels)
    # =========================================================================
    with st.expander("⚔️ Section 1: Campaign Setting & Classification", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            quest_title = st.text_input("Quest Title (Optional)", placeholder="e.g. The Drowned Reliquary of Aethelgard")
            game_genre = st.selectbox("World / Game Genre", options=GAME_GENRES, index=0)
            quest_type = st.selectbox("Quest Classification", options=QUEST_TYPES, index=0)
        with col2:
            theme = st.selectbox("Campaign Theme", options=QUEST_THEMES, index=1)
            difficulty = st.selectbox("Difficulty Rating", options=EXTENDED_DIFFICULTIES, index=1)
            missions = st.slider("Milestone Stages", min_value=1, max_value=6, value=3)

    with st.expander("🗺️ Section 2: World Geography, Lore & Setting", expanded=False):
        w_col1, w_col2 = st.columns(2)
        with w_col1:
            setting = st.text_input(
                "World / Level Setting",
                value="Submerged cathedral ruins of the Sunken Coast"
            )
            main_character = st.text_input(
                "Protagonist / Player Role",
                value="Aria the Tide Hunter, a specialist in abyssal relics"
            )
        with w_col2:
            lore_context = st.text_input(
                "Background Lore Directives",
                placeholder="e.g. The cathedral sank during the Great Lunar Flood 400 years ago"
            )
            narrative_tone = st.text_input(
                "Narrative Tone",
                value="Atmospheric, suspenseful, and rich in ancient mystery"
            )

    with st.expander("🛡️ Section 3: Objectives, Encounters & Rewards", expanded=True):
        o_col1, o_col2 = st.columns(2)
        with o_col1:
            quest_objective = st.text_area(
                "Primary Quest Objective",
                value=initial_idea or "Retrieve the Crystalline Coral Heart from the drowned crypts before the abyssal tide seals the chamber forever.",
                height=80
            )
            secondary_objectives = st.text_input(
                "Secondary / Optional Objectives",
                placeholder="e.g. Decipher three glyphs of the Old Tide; avoid alarming the shrine sentinels"
            )
        with o_col2:
            npc_characters = st.text_input(
                "NPCs & Allies",
                value="Brother Malakar, the last surviving monk of the coastal abbey"
            )
            enemies_encounters = st.text_input(
                "Enemies & Hazards",
                value="Abyssal Lurkers, crushing water pressure, and shifting coral labyrinths"
            )
            rewards = st.text_input(
                "Loot & Lore Rewards",
                value="Astrolabe of the Depths, 750 Gold Florins, and Codex of Tides"
            )

        additional_instructions = st.text_input(
            "Encounter Mechanics & Game Directives (Optional)",
            placeholder="e.g. Include oxygen-gauge mechanics and an ancient puzzle door"
        )

        st.markdown("<h5 style='margin-top: 0.8rem; color: var(--accent-olive);'>🖼️ Visual Reference (Optional)</h5>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Upload reference illustration (JPG, PNG — Max 5 MB)",
            type=["jpg", "jpeg", "png"],
            key="quest_ref_file"
        )
        if uploaded_file:
            st.caption(f"Loaded: {uploaded_file.name}")
        elif ref_image_path:
            st.caption(f"Using reference image from Image Studio: `{ref_image_path}`")

    # =========================================================================
    # GENERATION ACTION
    # =========================================================================
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    if st.button("Architect RPG Quest Codex →", type="primary", use_container_width=True):
        if not quest_objective:
            st.error("Please provide a primary quest objective.")
        else:
            with st.spinner("NVIDIA Nemotron is designing your RPG quest codex..."):
                try:
                    active_ref = ref_image_path
                    if uploaded_file:
                        up_res = api_client.upload_image(uploaded_file, "reference")
                        active_ref = up_res.get("file_path")

                    combined_instructions = f"Classification: {quest_type}."
                    if secondary_objectives:
                        combined_instructions += f" Secondary Goals: {secondary_objectives}."
                    if npc_characters:
                        combined_instructions += f" NPCs: {npc_characters}."
                    if enemies_encounters:
                        combined_instructions += f" Enemies: {enemies_encounters}."
                    if rewards:
                        combined_instructions += f" Rewards: {rewards}."
                    if additional_instructions:
                        combined_instructions += f" {additional_instructions}"

                    raw_diff = difficulty.split(" ")[0].lower()
                    diff_map = {"apprentice": "Easy", "adventurer": "Medium", "veteran": "Hard", "mythic": "Hard"}
                    clean_diff = diff_map.get(raw_diff, "Medium")

                    payload = {
                        "title": quest_title or f"The Trial of {setting[:25]}",
                        "game_genre": game_genre,
                        "theme": theme,
                        "difficulty": clean_diff,
                        "setting": setting,
                        "main_character": main_character,
                        "missions_count": missions,
                        "ending_preference": "Twist Ending",
                        "quest_objective": quest_objective,
                        "additional_instructions": combined_instructions,
                        "reference_image_path": active_ref
                    }
                    res = api_client.generate_quest(payload)
                    st.session_state["generated_quest_data"] = res
                    st.toast("Quest codex successfully inscribed!")
                except Exception as e:
                    st.error(f"Quest generation failed: {str(e)}")

    # =========================================================================
    # GENERATED QUEST LAYOUT (9 Structured Sections from PART 11)
    # =========================================================================
    quest_data = st.session_state.get("generated_quest_data")
    if quest_data:
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        # Handle both direct API response {"data": {...}} and saved project record {"generated_content": {...}}
        content = quest_data.get("data") or quest_data.get("generated_content") or quest_data
        title_disp = content.get("title") or quest_data.get("title") or "Untitled Quest Codex"

        with st.container(border=True):
            st.markdown(f"""
                <div style="border-bottom: 1px solid rgba(195, 167, 123, 0.25); padding-bottom: 1rem; margin-bottom: 1.5rem;">
                    <div style="font-family: var(--font-sans); font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.16em; color: var(--accent-olive); font-weight: 700;">
                        RPG CAMPAIGN CODEX
                    </div>
                    <h1 style="font-family: var(--font-display); font-size: 2.2rem; color: var(--text-primary); margin: 0.2rem 0;">
                        {title_disp}
                    </h1>
                    <div style="font-family: var(--font-sans); font-size: 0.85rem; color: var(--text-muted);">
                        Genre: <span style="color: var(--accent-olive);">{content.get('game_genre', game_genre)}</span> &bull;
                        Difficulty: <span style="color: var(--accent-gold);">{content.get('difficulty', difficulty)}</span> &bull;
                        Setting: <span style="color: var(--parchment);">{content.get('setting', setting)}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            tab_codex, tab_npcs, tab_lore, tab_art = st.tabs([
                "Quest Codex & Milestones",
                "NPCs & Dialogues",
                "Encounters, Lore & Rewards",
                "Synthesize Illustration"
            ])

            with tab_codex:
                # 1. Quest Overview
                st.markdown("<h3 style='margin-top: 0;'>1. Quest Overview</h3>", unsafe_allow_html=True)
                st.markdown(f"<div class='story-prose'>{content.get('quest_description', '')}</div>", unsafe_allow_html=True)

                # 3 & 4. Main & Secondary Objectives
                st.markdown("<h3 style='margin-top: 1.4rem;'>2. Main Objectives & Milestones</h3>", unsafe_allow_html=True)
                obj_val = content.get("objectives", "")
                st.markdown(f"<div class='story-prose'>{obj_val}</div>", unsafe_allow_html=True)

                # 9. Completion Conditions
                st.markdown("<h3 style='margin-top: 1.4rem;'>3. Completion Conditions & Resolution</h3>", unsafe_allow_html=True)
                ending_val = content.get("ending") or content.get("endings", "")
                st.markdown(f"<div class='story-prose'>{ending_val}</div>", unsafe_allow_html=True)

            with tab_npcs:
                # 5 & 6. NPC Characters & Dialogues
                st.markdown("<h3 style='margin-top: 0;'>NPC Cast & Persona Profiles</h3>", unsafe_allow_html=True)
                npc_val = content.get("npcs") or content.get("npc_characters", "")
                st.markdown(f"<div class='story-prose'>{npc_val}</div>", unsafe_allow_html=True)

                st.markdown("<h3 style='margin-top: 1.4rem;'>Scripted NPC Dialogues</h3>", unsafe_allow_html=True)
                dialogue_val = content.get("dialogue") or content.get("dialogues", "")
                st.markdown(f"<div class='story-prose'>{dialogue_val}</div>", unsafe_allow_html=True)

            with tab_lore:
                # 2. Background Lore
                st.markdown("<h3 style='margin-top: 0;'>Background Lore & History</h3>", unsafe_allow_html=True)
                lore_val = content.get("background_story") or content.get("lore_background", "Ancient records speak of long-forgotten epochs.")
                st.markdown(f"<div class='story-prose'>{lore_val}</div>", unsafe_allow_html=True)

                # 7. Enemies & Encounters
                st.markdown("<h3 style='margin-top: 1.4rem;'>Enemies, Hazards & Boss Encounters</h3>", unsafe_allow_html=True)
                chal_val = content.get("challenges", "")
                st.markdown(f"<div class='story-prose'>{chal_val}</div>", unsafe_allow_html=True)

                # 8. Rewards
                st.markdown("<h3 style='margin-top: 1.4rem;'>Codex Rewards & Loot Tables</h3>", unsafe_allow_html=True)
                rew_val = content.get("rewards", "")
                st.markdown(f"<div class='story-prose'>{rew_val}</div>", unsafe_allow_html=True)

            with tab_art:
                st.markdown("<h3>Synthesize Quest Illustration (FLUX.1-dev)</h3>", unsafe_allow_html=True)
                st.caption("Generate an illustration based on this quest's world.")
                suggested_prompt = (
                    content.get("suggested_illustration_description")
                    or content.get("suggested_image_description")
                    or f"A dark fantasy environment of {content.get('setting', setting)}"
                )
                quest_art_prompt = st.text_area("Artwork Prompt", value=suggested_prompt, height=85)
                q_art_style = st.selectbox("Visual Art Style", options=["Dark Fantasy", "Classical Art", "Cinematic Environment", "Vintage Concept Art"], index=0)

                if st.button("Synthesize Quest Artwork →", type="primary", use_container_width=True):
                    with st.spinner("FLUX is painting the quest scene..."):
                        try:
                            img_res = api_client.generate_image({
                                "prompt": quest_art_prompt,
                                "art_style": q_art_style,
                                "mood": "Mysterious",
                                "project_id": quest_data.get("project_id")
                            })
                            st.session_state["quest_illustration"] = img_res
                            st.toast("Illustration synthesized and cataloged!")
                        except Exception as e:
                            st.error(f"Illustration generation failed: {str(e)}")

                quest_img = st.session_state.get("quest_illustration")
                if quest_img:
                    q_img_path = quest_img.get("file_path") or quest_img.get("image_path") or ""
                    st.image(f"{BACKEND_URL}/{q_img_path}", caption=f"FLUX Illustration: {q_art_style}", use_container_width=True)

            # Save / Export Actions
            st.markdown("<hr style='margin: 1.5rem 0; border-color: rgba(195, 167, 123, 0.2);'>", unsafe_allow_html=True)
            col_save1, col_save2 = st.columns([1, 1])
            with col_save1:
                if st.button("Save Quest to Collection 💾", type="primary", use_container_width=True):
                    with st.spinner("Recording in permanent archive..."):
                        try:
                            saved = api_client.save_project({
                                "title": title_disp,
                                "project_type": "GAME_QUEST",
                                "generated_content": content,
                                "reference_image_path": quest_data.get("reference_image_path")
                            })
                            st.session_state["selected_project_id"] = saved.get("id")
                            st.toast("Quest archived successfully!")
                            navigate_to("My Projects")
                        except Exception as e:
                            st.error(f"Failed to save quest: {str(e)}")
            with col_save2:
                if st.button("Regenerate Quest Blueprint ↻", use_container_width=True):
                    st.session_state["generated_quest_data"] = None
                    st.rerun()
