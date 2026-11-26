"""
Narrative Studio — Image Studio Page
Adheres to PART 12: Visual-First Creative Workspace & Vision-Language AI
"""

import streamlit as st
from PIL import Image
from frontend.config import ART_STYLES, MOODS, BACKEND_URL
from frontend.components.navigation import render_back_button, navigate_to
from frontend.components.page_header import render_page_header
from frontend.utils.assets import get_asset_base64

try:
    from frontend.services.api_client import api_client
except (ModuleNotFoundError, ImportError):
    from services.api_client import api_client

EDITORIAL_STYLES = [
    "Dark Academia Oil Painting",
    "Classical Renaissance Art",
    "Moody Cinematic",
    "Dark Fantasy Illustration",
    "Gothic Etching & Engraving",
    "Vintage Victorian Lithograph",
    "Impressionist Landscape"
]

EDITORIAL_MOODS = [
    "Atmospheric & Brooding",
    "Candlelit & Mysterious",
    "Serene & Scholarly",
    "Epic & Dramatic",
    "Haunting & Eerie",
    "Sublime & Antiquarian"
]


def render_image_studio():
    """Renders the Dark Academia Image Studio atelier."""
    render_back_button(current_page="Image Studio", section="Creative Studios")

    render_page_header(
        badge="ATELIER III &bull; VISUAL ARTS & VISION AI",
        title="Image Studio",
        subtitle="Give your imagination a visual form.",
        bg_asset="image_studio_bg.png",
        overlay_darkness=0.88
    )

    tab_understanding, tab_generation, tab_gallery = st.tabs([
        "Reference Image & Vision Analysis",
        "FLUX Artwork Synthesis",
        "Atelier Visual Gallery"
    ])

    # =========================================================================
    # SECTION 1: REFERENCE IMAGE & VISION ANALYSIS
    # =========================================================================
    with tab_understanding:
        col_up, col_prev = st.columns([1.2, 1])

        with col_up:
            st.markdown("<h3 style='margin-top: 0;'>Reference Image Ingestion</h3>", unsafe_allow_html=True)
            st.caption("Upload paintings, sketches, or atmosphere references for Nemotron Vision analysis.")

            uploaded_file = st.file_uploader(
                "Select Reference Image (PNG, JPG — Max 5 MB)",
                type=["png", "jpg", "jpeg"],
                key="img_studio_uploader"
            )

            question = st.text_input(
                "Specific Focus / Analysis Query (Optional)",
                placeholder="e.g. Identify architectural motifs, lighting, and narrative mood"
            )

            btn_c1, btn_c2 = st.columns(2)
            with btn_c1:
                analyze_clicked = st.button("Inspect with Nemotron Vision →", type="primary", use_container_width=True)
            with btn_c2:
                if st.button("Clear Reference Image", use_container_width=True):
                    st.session_state["image_analysis_result"] = None
                    st.session_state["current_reference_image"] = None
                    st.rerun()

        with col_prev:
            if uploaded_file:
                try:
                    pil_img = Image.open(uploaded_file)
                    st.image(uploaded_file, caption=f"Loaded: {uploaded_file.name}", use_container_width=True)
                    st.markdown(f"""
                        <div style="font-family: var(--font-sans); font-size: 0.8rem; color: var(--text-muted); background: var(--bg-card); padding: 0.6rem 0.8rem; border-radius: 4px; border: 1px solid var(--border-color); margin-top: 0.5rem;">
                            Dimensions: {pil_img.size[0]} &times; {pil_img.size[1]} px &bull; Format: {pil_img.format} &bull; Size: {uploaded_file.size / 1024:.1f} KB
                        </div>
                    """, unsafe_allow_html=True)
                except Exception:
                    st.image(uploaded_file, use_container_width=True)
            else:
                st.markdown("""
                    <div style="border: 1px dashed var(--border-color); border-radius: 6px; padding: 3rem 1.5rem; text-align: center; color: var(--text-muted); font-family: var(--font-reading);">
                        No reference image currently loaded in the easel. Upload an image on the left to inspect visual characteristics.
                    </div>
                """, unsafe_allow_html=True)

        # Trigger Analysis
        if analyze_clicked:
            if not uploaded_file:
                st.error("Please select a reference image to inspect.")
            else:
                with st.spinner("NVIDIA Nemotron Vision is examining your imagery..."):
                    try:
                        up_res = api_client.upload_image(uploaded_file, "reference")
                        img_path = up_res.get("file_path")
                        analysis = api_client.analyze_image(image_path=img_path, question=question)
                        st.session_state["image_analysis_result"] = analysis
                        st.session_state["current_reference_image"] = analysis["image_path"]
                        st.toast("Vision examination complete!")
                    except Exception as e:
                        st.error(f"Analysis failed: {str(e)}")

        # Display Analysis Output
        analysis = st.session_state.get("image_analysis_result")
        if analysis:
            st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)
            with st.container(border=True):
                st.markdown("<h3 style='margin-top: 0;'>Vision Analysis Findings</h3>", unsafe_allow_html=True)
                st.markdown(f"**Visual Overview:** {analysis.get('description', 'No description available.')}")
                st.markdown(f"**Visible Figures & Characters:** {analysis.get('visible_characters', 'None identified.')}")
                st.markdown(f"**Artifacts & Objects:** {analysis.get('objects', 'None identified.')}")
                st.markdown(f"**Setting & Atmosphere:** {analysis.get('environment', 'Unspecified setting.')}")
                st.markdown(f"**Palette & Lighting:** {analysis.get('colors_and_atmosphere', 'Classic chiaroscuro.')}")
                st.markdown(f"**Thematic Motifs:** {analysis.get('possible_themes', 'Literary drama.')}")
                st.markdown(f"**Seeded Ideas:** {analysis.get('story_ideas', 'Explore ancient knowledge.')}")

            # Creative Seed Transfer
            st.markdown("<h4 style='margin-top: 1.2rem; color: var(--accent-gold);'>Use Vision as Creative Inspiration Seed</h4>", unsafe_allow_html=True)
            t_col1, t_col2 = st.columns(2)
            with t_col1:
                if st.button("Transfer Inspiration to Story Generator →", use_container_width=True):
                    st.session_state["story_seed_idea"] = analysis.get("story_ideas", "")
                    navigate_to("Story Generator")
            with t_col2:
                if st.button("Transfer Inspiration to Quest Generator →", use_container_width=True):
                    st.session_state["quest_seed_idea"] = analysis.get("story_ideas", "")
                    navigate_to("Quest Generator")

    # =========================================================================
    # SECTION 2: FLUX ARTWORK SYNTHESIS
    # =========================================================================
    with tab_generation:
        st.markdown("<h3 style='margin-top: 0;'>Classical Illustration Synthesis (FLUX.1-dev)</h3>", unsafe_allow_html=True)
        st.caption("Synthesize bespoke paintings, landscapes, and character portraits via hosted NVIDIA FLUX.")

        col_g1, col_g2 = st.columns(2)
        with col_g1:
            gen_prompt = st.text_area(
                "Prompt Description",
                value="An antique reading hall illuminated by candlelight, towering mahogany shelves lined with leather-bound grimoires, dust particles glowing in golden sunbeams",
                height=110
            )
            art_style = st.selectbox("Aesthetic Style", options=EDITORIAL_STYLES, index=0)
            mood = st.selectbox("Atmospheric Mood", options=EDITORIAL_MOODS, index=0)

        with col_g2:
            character_details = st.text_input(
                "Character Details (Optional)",
                placeholder="e.g. Rogue scholar in dark velvet robes examining an astrolabe"
            )
            environment_details = st.text_input(
                "Environment Details (Optional)",
                placeholder="e.g. Vaulted stained glass windows, midnight rain outside"
            )
            aspect_ratio = st.selectbox("Composition Aspect", options=["Widescreen Landscape (16:9)", "Classical Portrait (4:5)", "Square Folio (1:1)"], index=0)

        if st.button("Synthesize Artwork via FLUX →", type="primary", use_container_width=True):
            if not gen_prompt:
                st.error("Please provide a prompt description.")
            else:
                with st.spinner("FLUX is painting your classical masterpiece..."):
                    try:
                        res = api_client.generate_image({
                            "prompt": gen_prompt,
                            "art_style": art_style,
                            "mood": mood,
                            "character_details": character_details,
                            "environment_details": environment_details,
                            "aspect_ratio": aspect_ratio
                        })
                        st.session_state["studio_generated_image"] = res
                        st.toast("Artwork generated successfully!")
                    except Exception as e:
                        st.error(f"Image generation failed: {str(e)}")

        generated = st.session_state.get("studio_generated_image")
        if generated:
            st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)
            img_rel_path = generated.get("file_path") or generated.get("image_path") or ""
            img_url = f"{BACKEND_URL}/{img_rel_path}"

            c_disp1, c_disp2 = st.columns([1.5, 1])
            with c_disp1:
                st.image(img_url, caption=f"Style: {art_style} | Model: {generated.get('model_used')}", use_container_width=True)
            with c_disp2:
                with st.container(border=True):
                    st.markdown("<h4 style='color: var(--accent-gold); margin-top: 0;'>Masterpiece Details</h4>", unsafe_allow_html=True)
                    st.markdown(f"**Prompt:** {generated.get('prompt_used')}")
                    st.markdown(f"**Model:** `{generated.get('model_used')}`")

                    try:
                        import requests
                        r = requests.get(img_url)
                        if r.ok:
                            st.download_button(
                                label="Download PNG Image 📥",
                                data=r.content,
                                file_name="narrative_studio_illustration.png",
                                mime="image/png",
                                use_container_width=True
                            )
                    except Exception:
                        pass

    # =========================================================================
    # SECTION 3: ATELIER VISUAL GALLERY
    # =========================================================================
    with tab_gallery:
        st.markdown("<h3 style='margin-top: 0;'>Curated Visual Gallery</h3>", unsafe_allow_html=True)
        st.caption("Visual artwork generated across your creative projects and studio sessions.")

        try:
            all_projs = api_client.list_projects()
        except Exception:
            all_projs = []

        all_images = []
        for p in all_projs:
            for img in p.get("images", []):
                all_images.append({
                    "title": p.get("title", "Untitled Artwork"),
                    "path": img.get("file_path") or img.get("image_path") or "",
                    "type": img.get("image_type", "ILLUSTRATION"),
                    "prompt": img.get("image_prompt", "")
                })

        if not all_images:
            st.info("No illustrations stored in your projects yet. Generate illustrations in Story, Quest, or Image Studio.")
        else:
            grid_cols = st.columns(3)
            for idx, item in enumerate(all_images):
                with grid_cols[idx % 3]:
                    with st.container(border=True):
                        st.image(f"{BACKEND_URL}/{item['path']}", use_container_width=True)
                        st.markdown(f"<div style='font-family: var(--font-display); font-weight: 600; color: var(--text-primary);'>{item['title']}</div>", unsafe_allow_html=True)
                        st.caption(f"Category: {item['type']}")
