"""
Narrative Studio — Root Application Entrypoint
Allows launching directly via: streamlit run app.py
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = ROOT_DIR / "frontend"

for p in (str(ROOT_DIR), str(FRONTEND_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

# Execute the main frontend application
import frontend.app
