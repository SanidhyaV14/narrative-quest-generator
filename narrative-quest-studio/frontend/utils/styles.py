"""
Narrative Studio — Centralized Design Tokens & Styles
Dark Academia + Antique University Library + Luxury Editorial System
"""

# Exact Color Palette Tokens from Design System Specification
COLORS = {
    "PRIMARY_BG": "#11130F",       # Deep Forest-Black
    "SECONDARY_BG": "#1B2019",     # Dark Olive-Black
    "SIDEBAR_BG": "#171914",       # Deep Antique Surface
    "CARD_BG": "#24271F",          # Deep Forest Card
    "ELEVATED_SURFACE": "#303329", # Elevated Container Surface
    "BORDER": "#454438",           # Low-Contrast Antique Neutral
    "DARK_WALNUT": "#514034",      # Dark Walnut
    "BRONZE": "#806044",           # Antique Bronze
    "ANTIQUE_GOLD": "#C3A77B",     # Refined Antique Gold Accent
    "ANTIQUE_GOLD_HOVER": "#D4BD94", # Hover State
    "PARCHMENT": "#D8CCB4",        # Warm Parchment
    "PRIMARY_TEXT": "#F0E9D9",     # Ivory Header & Primary Text
    "SECONDARY_TEXT": "#B9B09B",   # Soft Parchment Secondary Text
    "MUTED_TEXT": "#898475",       # Muted Charcoal-Olive Text
    "MUTED_OLIVE": "#747C60",      # Active Navigation & Olive Accent
}

# Typography Hierarchy
FONTS = {
    "DISPLAY": "'Cormorant Garamond', 'Playfair Display', Georgia, serif",
    "SECTION": "'Playfair Display', 'Cormorant Garamond', Georgia, serif",
    "READING": "'Lora', 'Cormorant Garamond', Georgia, serif",
    "FUNCTIONAL": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
}

FONT_IMPORTS_HTML = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400;1,600&family=Inter:wght@300;400;500;600;700&family=Lora:ital,wght@0,400;0,500;0,600;1,400&family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
"""

GLOBAL_CSS = f"""
/* ====================================================================
   NARRATIVE STUDIO — MASTER DARK ACADEMIA STYLESHEET
   ==================================================================== */
:root {{
    --bg-primary: {COLORS['PRIMARY_BG']};
    --bg-secondary: {COLORS['SECONDARY_BG']};
    --bg-sidebar: {COLORS['SIDEBAR_BG']};
    --bg-card: {COLORS['CARD_BG']};
    --surface-elevated: {COLORS['ELEVATED_SURFACE']};
    --border-color: {COLORS['BORDER']};
    --dark-walnut: {COLORS['DARK_WALNUT']};
    --bronze: {COLORS['BRONZE']};
    --accent-gold: {COLORS['ANTIQUE_GOLD']};
    --accent-gold-hover: {COLORS['ANTIQUE_GOLD_HOVER']};
    --parchment: {COLORS['PARCHMENT']};
    --text-primary: {COLORS['PRIMARY_TEXT']};
    --text-secondary: {COLORS['SECONDARY_TEXT']};
    --text-muted: {COLORS['MUTED_TEXT']};
    --accent-olive: {COLORS['MUTED_OLIVE']};

    --font-display: {FONTS['DISPLAY']};
    --font-section: {FONTS['SECTION']};
    --font-reading: {FONTS['READING']};
    --font-sans: {FONTS['FUNCTIONAL']};
}}

/* ====================================================================
   SUPPRESS STREAMLIT DEPLOY BUTTON, TOOLBAR & SYSTEM CHROME
   ==================================================================== */
header,
header[data-testid="stHeader"],
[data-testid="stHeader"],
.stDeployButton,
[data-testid="stDeployButton"],
[data-testid="stAppDeployButton"],
[data-testid="stToolbar"],
[data-testid="stToolbarActions"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
#MainMenu,
footer,
button[title="View app in Streamlit Community Cloud"],
button[aria-label="View app in Streamlit Community Cloud"],
button[data-testid="stHeaderMenuButton"],
div[data-testid="stToolbar"],
div[class*="viewerBadge"],
div[class*="deployButton"],
div[class*="stToolbarActions"],
.viewerBadge_container__1QSob,
.styles_viewerBadge__CvCqN,
[data-testid="stSidebar"],
[data-testid="collapsedControl"],
section[data-testid="stSidebar"],
div[data-testid="stSidebarCollapsedControl"],
button[aria-label="Close sidebar"],
button[aria-label="Open sidebar"] {{
    display: none !important;
    visibility: hidden !important;
    height: 0px !important;
    width: 0px !important;
    opacity: 0 !important;
    pointer-events: none !important;
    overflow: hidden !important;
    margin: 0 !important;
    padding: 0 !important;
}}

.stApp > header {{
    display: none !important;
    height: 0 !important;
}}

.stApp [data-testid="stSidebar"] + section.main,
.stApp section.main {{
    margin-left: 0 !important;
    width: 100% !important;
}}

/* ====================================================================
   BASE CANVAS & CONTAINER LAYOUT
   ==================================================================== */
.stApp {{
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: var(--font-reading) !important;
}}

.main .block-container {{
    padding-top: 1rem !important;
    padding-bottom: 3rem !important;
    max-width: 1220px !important;
}}

/* ====================================================================
   TYPOGRAPHY SYSTEM
   ==================================================================== */
h1, .page-title, .hero-title {{
    font-family: var(--font-display) !important;
    color: var(--text-primary) !important;
    font-weight: 700 !important;
    font-size: 2.35rem !important;
    letter-spacing: 0.02em !important;
    line-height: 1.2 !important;
    margin-bottom: 0.35rem !important;
    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.7);
}}

h2, .section-title {{
    font-family: var(--font-section) !important;
    font-size: 1.65rem !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
    letter-spacing: 0.02em !important;
    margin-top: 1.4rem !important;
    margin-bottom: 0.6rem !important;
    border-bottom: 1px solid rgba(195, 167, 123, 0.22);
    padding-bottom: 0.4rem;
}}

h3, .sub-section-title {{
    font-family: var(--font-display) !important;
    font-size: 1.3rem !important;
    font-weight: 600 !important;
    color: var(--accent-gold) !important;
    letter-spacing: 0.02em !important;
    margin-bottom: 0.35rem !important;
}}

h4, h5, h6 {{
    font-family: var(--font-display) !important;
    letter-spacing: 0.03em !important;
    color: var(--text-primary) !important;
}}

p, span, label, div {{
    color: var(--text-primary);
}}

.stMarkdown p, .stMarkdown li {{
    font-family: var(--font-reading) !important;
    font-size: 1.05rem !important;
    line-height: 1.75 !important;
    color: var(--text-primary) !important;
}}

.story-prose, .manuscript-body {{
    font-family: var(--font-reading) !important;
    font-size: 1.15rem !important;
    line-height: 1.85 !important;
    color: var(--text-primary) !important;
    letter-spacing: 0.01em;
}}

.text-parchment {{
    color: var(--parchment) !important;
}}

.text-muted {{
    color: var(--text-muted) !important;
    font-size: 0.88rem;
    font-family: var(--font-sans) !important;
}}

.text-gold {{
    color: var(--accent-gold) !important;
}}

.text-olive {{
    color: var(--accent-olive) !important;
}}

/* ====================================================================
   SIDEBAR STYLING
   ==================================================================== */
[data-testid="stSidebar"] {{
    background-color: var(--bg-sidebar) !important;
    border-right: 1px solid var(--border-color) !important;
}}

[data-testid="stSidebar"] p, [data-testid="stSidebar"] span {{
    font-family: var(--font-sans) !important;
}}

/* ====================================================================
   BUTTONS (Editorial Roman & Antique Gold Accents)
   ==================================================================== */
.stButton > button {{
    font-family: var(--font-sans) !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.04em !important;
    border-radius: 5px !important;
    padding: 0.45rem 1rem !important;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    border: 1px solid var(--border-color) !important;
    background-color: var(--bg-card) !important;
    color: var(--text-primary) !important;
}}

.stButton > button:hover {{
    transform: translateY(-1px);
    border-color: var(--accent-gold) !important;
    color: var(--accent-gold) !important;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.45);
}}

.stButton > button[kind="primary"] {{
    background-color: var(--accent-gold) !important;
    color: #11130F !important;
    font-weight: 700 !important;
    border: 1px solid var(--accent-gold) !important;
    letter-spacing: 0.06em !important;
}}

.stButton > button[kind="primary"]:hover {{
    background-color: var(--accent-gold-hover) !important;
    color: #11130F !important;
    box-shadow: 0 4px 16px rgba(195, 167, 123, 0.35) !important;
}}

/* Secondary / Subdued Button */
.stButton > button[kind="secondary"] {{
    background-color: var(--bg-secondary) !important;
    border-color: var(--border-color) !important;
}}

/* ====================================================================
   INPUTS, SELECTBOXES & EXPANDERS
   ==================================================================== */
.stTextInput input, .stTextArea textarea, .stSelectbox select {{
    background-color: var(--bg-card) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 5px !important;
    font-family: var(--font-sans) !important;
    font-size: 0.95rem !important;
}}

.stTextInput input:focus, .stTextArea textarea:focus {{
    border-color: var(--accent-gold) !important;
    box-shadow: 0 0 0 1px var(--accent-gold) !important;
}}

.stSelectbox label, .stTextInput label, .stTextArea label, .stSlider label {{
    font-family: var(--font-sans) !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    color: var(--parchment) !important;
    text-transform: uppercase !important;
}}

/* Streamlit Containers & Cards */
[data-testid="stVerticalBlockBorderWrapper"] {{
    border-color: var(--border-color) !important;
    background-color: var(--bg-card) !important;
    border-radius: 6px !important;
}}

/* Streamlit Tabs */
.stTabs [data-baseweb="tab-list"] {{
    border-bottom: 1px solid var(--border-color) !important;
    gap: 1.5rem;
}}

.stTabs [data-baseweb="tab"] {{
    color: var(--text-muted) !important;
    font-family: var(--font-display) !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.04em !important;
    padding: 0.6rem 0.2rem !important;
}}

.stTabs [aria-selected="true"] {{
    color: var(--accent-gold) !important;
    border-bottom: 2px solid var(--accent-gold) !important;
    font-weight: 700;
}}

/* Streamlit Metrics */
[data-testid="stMetricValue"] {{
    font-family: var(--font-display) !important;
    color: var(--accent-gold) !important;
    font-size: 2.1rem !important;
    font-weight: 700 !important;
}}

[data-testid="stMetricLabel"] {{
    color: var(--text-muted) !important;
    font-family: var(--font-sans) !important;
    font-size: 0.78rem !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}}

/* Streamlit Expanders */
.streamlit-expanderHeader {{
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 6px !important;
    font-family: var(--font-display) !important;
    font-size: 1.05rem !important;
    color: var(--text-primary) !important;
}}

/* ====================================================================
   DARK ACADEMIA CARDS & HERO PANELS
   ==================================================================== */
.editorial-hero-banner {{
    position: relative;
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid var(--border-color);
    background-size: cover;
    background-position: center;
    min-height: 270px;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    padding: 2.2rem;
    margin-bottom: 1.8rem;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.6);
}}

.editorial-hero-banner::before {{
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(180deg, rgba(17, 19, 15, 0.4) 0%, rgba(17, 19, 15, 0.94) 85%);
    z-index: 1;
}}

.editorial-hero-content {{
    position: relative;
    z-index: 2;
    max-width: 680px;
}}

.studio-feature-card {{
    background-color: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 6px;
    padding: 1.4rem;
    min-height: 220px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: all 0.25s ease;
    background-size: cover;
    background-position: center;
    position: relative;
    overflow: hidden;
}}

.studio-feature-card::before {{
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(180deg, rgba(36, 39, 31, 0.85) 0%, rgba(36, 39, 31, 0.98) 100%);
    z-index: 1;
}}

.studio-card-inner {{
    position: relative;
    z-index: 2;
}}

.studio-feature-card:hover {{
    border-color: var(--accent-gold);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.5);
}}

.badge-tag {{
    font-family: var(--font-sans);
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-weight: 700;
    margin-bottom: 0.35rem;
    display: inline-block;
}}

.badge-gold {{ color: var(--accent-gold); }}
.badge-bronze {{ color: var(--bronze); }}
.badge-olive {{ color: var(--accent-olive); }}

/* Reduced Motion */
@media (prefers-reduced-motion: reduce) {{
    * {{
        transition: none !important;
        animation: none !important;
        transform: none !important;
    }}
}}
"""
