# Software Requirements Specification (SRS)
## Narrative Studio: A Multimodal AI-Powered Story and Game Quest Generator

---

### 1. Introduction

#### 1.1 Purpose
This document specifies the software requirements for **Narrative Studio**, a multimodal web application engineered for creative writers, world-builders, and indie game developers. It enables text generation, vision-language analysis, and illustration rendering powered by NVIDIA-hosted AI models.

#### 1.2 Scope
Narrative Studio provides:
- Structured creative story generation (genres, tones, characters, multi-act narratives).
- Structured video-game RPG quest generation (mission stages, lore, NPCs, dialogue, rewards, obstacles).
- Reference image visual analysis using NVIDIA Nemotron vision-language capabilities.
- AI illustration synthesis using NVIDIA FLUX.1-dev.
- Persistent project management, user ownership isolation, and plain-text export.

---

### 2. Overall Description

#### 2.1 Product Perspective
Narrative Studio is a modern decoupled web application:
- **Frontend Layer:** Streamlit (Python 3.11+) delivering a dark-navy responsive creative interface.
- **Backend API Layer:** FastAPI web server implementing JWT authentication, input validation, and asynchronous external AI routing.
- **Database & Storage Layer:** MySQL 8.x (with resilient local SQLite fallback) via SQLAlchemy 2.x ORM, alongside secure local disk storage for image assets.
- **AI Service Layer:** NVIDIA Build endpoints hosting Nemotron and FLUX models.

#### 2.2 User Characteristics
- **Creative Writers:** Require atmospheric settings, character development, and narrative arcs.
- **Game Designers & Quest Writers:** Require structured quest logs, balanced objectives, challenges, and NPC interactions.
- **Students & Content Creators:** Require multimodal inspiration from reference images to kickstart creative writing.

---

### 3. Functional Requirements

#### 3.1 User Management (FR-01)
- **FR-01.1 Registration:** New users can register with username, unique email address, and password (minimum 6 characters). Passwords must be hashed using bcrypt.
- **FR-01.2 Login & JWT:** Registered users authenticate with email and password to receive a signed JWT token valid for 24 hours.
- **FR-01.3 Profile & Session:** Private API routes validate bearer tokens. Users can only read, modify, or delete their own projects.

#### 3.2 Multimodal Text Generation (FR-02)
- **FR-02.1 Story Generator:** Users configure genre, theme, setting, character, plot idea, length, and tone. Nemotron returns structured JSON containing title, introduction, characters, setting, conflict, story, ending, and an image prompt.
- **FR-02.2 Quest Generator:** Users configure game genre, theme, setting, difficulty, protagonist, objective, mission stages (1-10), and ending preference. Nemotron returns structured JSON containing quest title, description, backstory, NPCs, objectives, challenges, dialogue, rewards, ending, and illustration prompt.
- **FR-02.3 Visual Context Integration:** When a reference image is supplied, the vision-language analysis is injected into the generation prompt.

#### 3.3 Multimodal Image Studio (FR-03)
- **FR-03.1 Image Analysis:** Upload JPG/PNG images up to 5 MB. Pillow validates file format and integrity. Nemotron vision model inspects visual elements (characters, objects, environment, palette, themes, story ideas).
- **FR-03.2 Creative Transfer:** Users can directly seed Story or Quest generators with ideas extracted from image analysis.
- **FR-03.3 Illustration Generation:** Users submit text prompts, style, and mood to the FLUX.1-dev endpoint. Generated images are saved locally to `uploads/generated/` and linked to projects.

#### 3.4 Project Management & Export (FR-04)
- **FR-04.1 Saving:** Saves project metadata, user inputs, structured content, and image paths.
- **FR-04.2 History & Filtering:** View saved projects filtered by type (`STORY` vs `GAME_QUEST`).
- **FR-04.3 TXT Export:** Download formatted text documents containing inputs, story/quest content, and image paths.
- **FR-04.4 Deletion:** Delete projects and automatically clean up associated local image files.
- **FR-04.5 Feedback:** Submit a 1-5 star rating and comment for any owned project.

---

### 4. Non-Functional Requirements

- **Security (NFR-01):** Passwords hashed with bcrypt (salt rounds >= 12); no plain-text storage. JWT HMAC-SHA256 tokens. Path sanitization prevents directory traversal. File size enforced at 5 MB.
- **Performance (NFR-02):** Backend responses for local database CRUD under 100 ms. AI requests configured with configurable timeouts (60s Nemotron, 90s FLUX).
- **Usability (NFR-03):** Streamlit interface with dark theme `#0b0f19`, clear card layouts, loading spinners, and error alerts. Avoids displaying raw JSON.
- **Maintainability (NFR-04):** Clean separation of concerns across `backend/routes`, `backend/services`, `backend/ai`, `backend/models`, and `frontend/pages`.
