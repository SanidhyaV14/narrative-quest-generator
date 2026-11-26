# Narrative Studio
## A Multimodal AI-Powered Story and Game Quest Generator

[![Python Version](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.15-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B.svg)](https://streamlit.io/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red.svg)](https://www.sqlalchemy.org/)
[![Tests](https://img.shields.io/badge/pytest-20%20passed-success.svg)](docs/TEST_REPORT.md)

---

## 1. Abstract
**Narrative Studio** is a multimodal AI-assisted creative suite that bridges text generation, vision-language understanding, and illustration synthesis into a unified web application. Developed for creative writers, world-builders, and indie game developers, the platform leverages NVIDIA-hosted AI models—**NVIDIA Nemotron** for narrative reasoning & image understanding and **FLUX.1-dev** for visual illustration—enabling creators to transform abstract ideas and reference imagery into structured, publishable stories and playable video-game quests.

---

## 2. Problem Statement
Creative writing and game design often stall at the brainstorming and conceptualization stage. Writers struggle with narrative pacing and conflict structuring, while indie game developers frequently lack the specialized tools to build coherent quest logs with balanced objectives, NPC dialogues, lore, and rewards. Furthermore, existing AI tools are largely fragmented: text generation, image inspection, and concept art generation live in separate silos with no cohesive project management, ownership protection, or local export capabilities.

---

## 3. Project Objectives
1. Provide an intuitive, modern web application for generating structured stories and game quests.
2. Implement **Image Understanding** using NVIDIA Nemotron vision-language models to extract characters, environment, atmosphere, and story seeds from uploaded artwork.
3. Integrate **Image Generation** using NVIDIA-hosted FLUX models to synthesize custom concept illustrations for stories and quests.
4. Deliver a secure, multi-tenant backend architecture with JWT authentication, bcrypt password hashing, and user project isolation.
5. Provide persistent project storage with MySQL 8.x (and automatic local SQLite fallback), image asset management, and plain-text export.

---

## 4. Key Features
- **Multimodal Text-to-Story Generation:** Generate rich multi-act narratives with custom genres, tones, lengths, character arcs, and suggested illustration prompts.
- **Game Quest Generator:** Produce game-ready RPG quests featuring background lore, step-by-step milestones, difficulty levels, NPC dialogues, challenges, and rewards.
- **Image Understanding Studio (Section A):** Upload JPG/PNG reference images (up to 5 MB) for automated vision analysis detailing visible characters, objects, color palettes, and creative narrative seeds.
- **Illustration Studio (Section B):** Synthesize high-resolution concept art using FLUX.1-dev with customizable art styles (Fantasy, Digital Painting, Anime, Realistic, Concept Art) and moods.
- **Project Persistence & History:** Save stories and quests to MySQL/SQLite, filter by type, view associated illustrations, and submit feedback ratings (1 to 5 stars).
- **One-Click TXT Export:** Download formatted, clean text documents of any saved project.
- **Secure Architecture:** Bcrypt password hashing, JWT bearer authentication, user ownership isolation, and image directory traversal protection.

---

## 5. Technology Stack

| Layer | Technology | Version | Purpose |
|---|---|---|---|
| **Language** | Python | 3.11+ / 3.15 | Core development language |
| **Frontend** | Streamlit | 1.32+ | Interactive, dark-themed creative UI |
| **Backend API** | FastAPI / Uvicorn | 0.110+ / 0.28+ | High-performance ASGI web framework |
| **Database** | MySQL 8.x / SQLite | 8.x / 3.x | Relational data persistence with automatic fallback |
| **ORM** | SQLAlchemy | 2.0+ | Database models and session management |
| **Data Validation** | Pydantic | 2.6+ | Request and response schema enforcement |
| **AI Models (Text & Vision)** | NVIDIA Nemotron | 4 340B / 3.5 VL | Story generation, quest generation, vision understanding |
| **AI Models (Image Gen)** | FLUX.1-dev | Hosted | Illustration synthesis |
| **Security & Auth** | PyJWT & Bcrypt | 2.8+ / 4.1+ | Token authorization and password hashing |
| **Image Processing** | Pillow (PIL) | 10.2+ | Image verification, format checking, and dimensions |
| **Testing** | pytest & pytest-asyncio | 8.1+ / 0.23+ | Automated unit and end-to-end integration testing |

---

## 6. System Architecture

```mermaid
flowchart TD
    subgraph Frontend["Streamlit Frontend (Port 8501)"]
        UI_Auth[Login / Register]
        UI_Dash[Dashboard]
        UI_Story[Story Generator]
        UI_Quest[Quest Generator]
        UI_Img[Image Studio]
        UI_Proj[My Projects & TXT Export]
    end

    subgraph Backend["FastAPI Backend (Port 8000)"]
        API_Auth[Auth Routes - JWT & Bcrypt]
        API_Gen[Generation Routes]
        API_Img[Image Routes & Local Storage]
        API_Proj[Projects & Feedback Routes]
    end

    subgraph AI["NVIDIA AI Service Layer"]
        Nemotron[Nemotron VL / Text Client]
        Flux[FLUX Image Generation Client]
        Templates[Prompt Templates]
    end

    subgraph DB["Storage Layer"]
        SQL[(MySQL / SQLite Fallback)]
        Disk[(Local Uploads: references/ & generated/)]
    end

    Frontend -->|HTTP / JSON + JWT| Backend
    Backend --> AI
    Backend --> DB
```

---

## 7. Project Folder Structure

```text
NarrativeStudio/
├── frontend/
│   ├── app.py                      # Main Streamlit app with dark theme & routing
│   ├── config.py                   # Frontend constants, genres, themes, moods
│   ├── pages/
│   │   ├── login.py                # User login page
│   │   ├── register.py             # User registration page
│   │   ├── dashboard.py            # Dashboard with metrics and studio cards
│   │   ├── story_generator.py      # Story generator UI & export
│   │   ├── quest_generator.py      # Game quest generator UI & export
│   │   ├── image_studio.py         # Vision analysis & FLUX generation
│   │   └── my_projects.py          # Project management, filtering & feedback
│   └── services/
│       └── api_client.py           # Backend communication client
│
├── backend/
│   ├── main.py                     # FastAPI entry point, CORS, static file mounts
│   ├── config.py                   # Pydantic BaseSettings & environment variables
│   ├── database.py                 # SQLAlchemy engine with MySQL & SQLite fallback
│   ├── init_db.py                  # Database initialization and demo seeding script
│   ├── models/
│   │   ├── __init__.py             # Model exports
│   │   ├── user.py                 # Users model
│   │   ├── project.py              # Projects model
│   │   ├── project_image.py        # Project images model
│   │   ├── generation_history.py   # AI generation history log model
│   │   └── feedback.py             # Project feedback & ratings model
│   ├── schemas/
│   │   ├── auth.py                 # Auth request/response schemas
│   │   ├── story.py                # Story generation schemas
│   │   ├── quest.py                # Quest generation schemas
│   │   └── project.py              # Project, image & feedback schemas
│   ├── routes/
│   │   ├── auth.py                 # Register, login, me endpoints
│   │   ├── generation.py           # Story & quest generation routes
│   │   ├── images.py               # Image analysis & generation routes
│   │   ├── projects.py             # Project CRUD & TXT export routes
│   │   └── feedback.py             # Rating and feedback routes
│   ├── ai/
│   │   ├── nemotron_client.py      # NVIDIA Nemotron text and vision client
│   │   ├── flux_client.py          # NVIDIA FLUX image generation client
│   │   └── prompt_templates.py     # Structured JSON prompt engineering
│   └── utils/
│       ├── security.py             # Bcrypt hashing & JWT token validation
│       ├── file_handler.py         # Safe image saving, base64 & disk cleanup
│       └── validators.py           # Email, format & file size validators
│
├── database/
│   ├── schema.sql                  # MySQL 8.x schema DDL with indexes & FKs
│   └── seed.sql                    # Seed script with demo user & sample projects
│
├── uploads/
│   ├── references/                 # Local storage for user reference images
│   └── generated/                  # Local storage for AI-generated illustrations
│
├── tests/
│   ├── conftest.py                 # Pytest test fixtures & mock test client
│   ├── test_auth.py                # TC01 - TC04: Authentication tests
│   ├── test_generation.py          # TC05 - TC06, TC17: Story & quest AI tests
│   ├── test_images.py              # TC07 - TC11: Image upload & FLUX tests
│   ├── test_projects.py            # TC12 - TC16: Project CRUD, isolation & export
│   └── test_e2e_workflows.py       # End-to-end multimodal workflow tests (A, B, C)
│
├── docs/
│   ├── SRS.md                      # Software Requirements Specification
│   ├── ARCHITECTURE_AND_UML.md     # UML Diagrams (Architecture, ER, Use Case, Sequence)
│   └── TEST_REPORT.md              # Automated test execution report
│
├── .env.example                    # Environment variable configuration template
├── .gitignore                      # Git exclusion rules
├── pytest.ini                      # Pytest runner configuration
├── requirements.txt                # Python package dependencies
└── README.md                       # Master project documentation
```

---

## 8. Database Schema

The database consists of 5 normalized tables in `database/schema.sql`:

1. `users`: Stores user credentials (`id`, `username`, `email`, `password_hash`, `created_at`).
2. `projects`: Stores projects owned by users (`id`, `user_id`, `title`, `project_type`, `input_data`, `generated_content`, `created_at`, `updated_at`).
3. `project_images`: Tracks associated uploaded reference or generated images (`id`, `project_id`, `image_type`, `file_path`, `image_prompt`, `image_description`, `created_at`).
4. `generation_history`: Audit trail for AI generation operations (`id`, `project_id`, `operation_type`, `model_name`, `input_prompt`, `created_at`).
5. `project_feedback`: User ratings and comments (`id`, `project_id`, `user_id`, `rating`, `comments`, `created_at`).

---

## 9. API Endpoint Reference

| Category | Method | Endpoint | Description | Protected |
|---|---|---|---|---|
| **Health** | `GET` | `/api/health` | Service health status | No |
| **Auth** | `POST` | `/api/auth/register` | Register new user | No |
| **Auth** | `POST` | `/api/auth/login` | Authenticate user & receive JWT | No |
| **Auth** | `GET` | `/api/auth/me` | Fetch authenticated user profile | Yes (JWT) |
| **Generation** | `POST` | `/api/generate/story` | Generate structured story via Nemotron | Yes (JWT) |
| **Generation** | `POST` | `/api/generate/quest` | Generate structured game quest | Yes (JWT) |
| **Images** | `POST` | `/api/images/analyze` | Upload and analyze image via Vision AI | Yes (JWT) |
| **Images** | `POST` | `/api/images/generate` | Synthesize illustration via FLUX | Yes (JWT) |
| **Projects** | `POST` | `/api/projects` | Save story or quest project | Yes (JWT) |
| **Projects** | `GET` | `/api/projects` | List projects (with type filter) | Yes (JWT) |
| **Projects** | `GET` | `/api/projects/{id}` | Get full project details | Yes (JWT) |
| **Projects** | `DELETE` | `/api/projects/{id}` | Delete project & clean image files | Yes (JWT) |
| **Projects** | `GET` | `/api/projects/{id}/export` | Export project as formatted TXT | Yes (JWT) |
| **Feedback** | `POST` | `/api/feedback` | Submit 1-5 star project rating | Yes (JWT) |

Interactive Swagger documentation is available at: `http://127.0.0.1:8000/docs`

---

## 10. AI Model Integration Details

1. **NVIDIA Nemotron (Text & Vision-Language):**
   - **Text Generation:** Uses NVIDIA Nemotron / OpenAI-compatible endpoint (`https://integrate.api.nvidia.com/v1`). Prompt engineering in `backend/ai/prompt_templates.py` enforces structured JSON outputs.
   - **Image Understanding:** Uses vision-language capabilities with base64 data URLs to analyze character appearance, environment, colors, atmosphere, and creative ideas.
2. **NVIDIA FLUX.1-dev (Image Generation):**
   - Uses NVIDIA-hosted endpoint (`https://ai.api.nvidia.com/v1/genai/black-forest-labs/flux-1-dev`).
   - Generates high-fidelity 1024x1024 illustrations based on enhanced prompts.
   - Results are automatically decoded from base64/URL and persisted to `uploads/generated/`.

---

## 11. Installation & Running Instructions

### Prerequisites
- Windows 11 (or macOS / Linux) with at least 8 GB RAM.
- Python 3.11 or newer.
- (Optional) MySQL 8.x (the system automatically uses local SQLite if MySQL is not running).

### Step 1: Clone or Open Workspace
```powershell
cd C:\Users\User\Documents\narrative-quest-studio
```

### Step 2: Set Up Virtual Environment & Dependencies
```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables
Copy `.env.example` to `.env`:
```powershell
Copy-Item .env.example .env
```
Open `.env` and set your configuration:
```env
# Database: Default SQLite fallback for zero-config development
DATABASE_URL=sqlite:///./narrative_studio.db

# If using MySQL 8.x:
# DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/narrative_studio

# NVIDIA API Key from https://build.nvidia.com/
NVIDIA_API_KEY=your_nvidia_api_key_here
```

### Step 4: Initialize the Database
```powershell
python -m backend.init_db
```
*This creates the database tables and seeds a demo account:*
- **Username:** `demo_writer`
- **Email:** `demo@narrativestudio.ai`
- **Password:** `password123`

### Step 5: Start the Backend (Terminal 1)
```powershell
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
- API Docs: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/api/health`

### Step 6: Start the Frontend (Terminal 2)
```powershell
streamlit run frontend/app.py
```
- Frontend UI: `http://localhost:8501`

---

## 12. Running Tests

Run the full pytest suite:
```powershell
.venv\Scripts\pytest.exe -v tests/
```
All **20 test cases** execute in ~10 seconds with **100% pass rate**:
- `test_auth.py`: TC01 – TC04
- `test_generation.py`: TC05, TC06, TC17
- `test_images.py`: TC07 – TC11
- `test_projects.py`: TC12 – TC16
- `test_e2e_workflows.py`: Complete Workflows A, B, and C

---

## 13. Known Limitations
- Model response times depend on NVIDIA Build hosted server loads (typically 3–8s for text, 15–30s for FLUX image synthesis).
- SQLite is active by default for immediate zero-config testing; production deployment should point to MySQL 8.x.

## 14. Future Enhancements
- Interactive branching dialogue trees for game quest generation.
- Direct JSON export compatible with game engines like Unity (ScriptableObjects) and Unreal Engine (Data Tables).
- Multi-character portrait galleries linked to quest log entries.
