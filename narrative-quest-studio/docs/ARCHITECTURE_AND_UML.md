# System Architecture & UML Diagrams
## Narrative Studio: Multimodal AI-Powered Story & Game Quest Generator

---

### 1. System Architecture Diagram

```mermaid
flowchart TD
    subgraph Client["Client Layer (Browser)"]
        UI["Streamlit Web UI (Port 8501)"]
        Pages["Login | Register | Dashboard | Story Gen | Quest Gen | Image Studio | My Projects"]
    end

    subgraph BackendLayer["Application & API Layer (FastAPI Port 8000)"]
        FastAPIApp["FastAPI ASGI Server"]
        AuthMiddleware["JWT Authentication & Security"]
        RouterAuth["/api/auth Router"]
        RouterGen["/api/generate Router"]
        RouterImg["/api/images Router"]
        RouterProj["/api/projects Router"]
        RouterFeed["/api/feedback Router"]
    end

    subgraph ServiceLayer["AI & Business Logic Services"]
        NemotronSvc["Nemotron Client (Text & Vision-Language)"]
        FluxSvc["FLUX Client (Image Generation)"]
        PromptEngine["Structured Prompt Templates"]
        FileHandler["File Handler (Pillow & Disk Storage)"]
    end

    subgraph ExternalAI["External NVIDIA Build Endpoints"]
        NV_Nemotron["NVIDIA Nemotron 4 340B / 3.5 VL"]
        NV_Flux["NVIDIA FLUX.1-dev Endpoint"]
    end

    subgraph Persistence["Storage & Database Layer"]
        SQL_DB[("MySQL 8.x / SQLite Fallback")]
        UploadDisk[("uploads/references & uploads/generated")]
    end

    UI -->|HTTP / JSON + Bearer Token| FastAPIApp
    FastAPIApp --> AuthMiddleware
    AuthMiddleware --> RouterAuth
    AuthMiddleware --> RouterGen
    AuthMiddleware --> RouterImg
    AuthMiddleware --> RouterProj
    AuthMiddleware --> RouterFeed

    RouterGen --> PromptEngine
    RouterGen --> NemotronSvc
    RouterImg --> NemotronSvc
    RouterImg --> FluxSvc
    RouterImg --> FileHandler

    NemotronSvc -->|HTTPS / OpenAI-Compatible JSON| NV_Nemotron
    FluxSvc -->|HTTPS / REST API| NV_Flux

    RouterProj --> SQL_DB
    RouterAuth --> SQL_DB
    RouterFeed --> SQL_DB
    FileHandler --> UploadDisk
```

---

### 2. Database Entity-Relationship (ER) Diagram

```mermaid
erDiagram
    USERS ||--o{ PROJECTS : "owns"
    USERS ||--o{ PROJECT_FEEDBACK : "submits"
    PROJECTS ||--o{ PROJECT_IMAGES : "contains"
    PROJECTS ||--o{ GENERATION_HISTORY : "tracks"
    PROJECTS ||--o{ PROJECT_FEEDBACK : "receives"

    USERS {
        int id PK
        varchar username
        varchar email UK
        varchar password_hash
        datetime created_at
    }

    PROJECTS {
        int id PK
        int user_id FK
        varchar title
        varchar project_type
        json input_data
        json generated_content
        datetime created_at
        datetime updated_at
    }

    PROJECT_IMAGES {
        int id PK
        int project_id FK
        varchar image_type
        varchar file_path
        text image_prompt
        text image_description
        datetime created_at
    }

    GENERATION_HISTORY {
        int id PK
        int project_id FK
        varchar operation_type
        varchar model_name
        text input_prompt
        datetime created_at
    }

    PROJECT_FEEDBACK {
        int id PK
        int project_id FK
        int user_id FK
        int rating
        text comments
        datetime created_at
    }
```

---

### 3. Use Case Diagram

```mermaid
flowchart LR
    User((User / Writer / Designer))

    subgraph NarrativeStudio["Narrative Studio System"]
        UC1["Register Account"]
        UC2["Login / Authenticate"]
        UC3["Generate Structured Story"]
        UC4["Generate Video Game Quest"]
        UC5["Analyze Reference Image (Vision AI)"]
        UC6["Generate AI Illustration (FLUX)"]
        UC7["Save & Manage Projects"]
        UC8["Export Project as TXT"]
        UC9["Submit Project Rating / Feedback"]
    end

    User --> UC1
    User --> UC2
    User --> UC3
    User --> UC4
    User --> UC5
    User --> UC6
    User --> UC7
    User --> UC8
    User --> UC9
```

---

### 4. Activity Diagram: Multimodal Generation Workflow

```mermaid
flowchart TD
    Start([User Starts Workflow]) --> SelectMode{Select Mode}

    SelectMode -->|Story Generator| StoryInput[Input Genre, Tone, Setting, Character, Premise]
    SelectMode -->|Quest Generator| QuestInput[Input Game Genre, Difficulty, Missions, Objective]
    SelectMode -->|Image Studio| ImageUpload[Upload JPG/PNG Image]

    ImageUpload --> ValidateImg[Validate Format & Size <= 5MB]
    ValidateImg --> VisionAI[Nemotron Vision Analyzes Image]
    VisionAI --> DisplayAnalysis[Display Characters, Atmosphere & Story Ideas]
    DisplayAnalysis --> TransferSeed[Use Ideas as Inspiration for Story/Quest]
    TransferSeed --> StoryInput

    StoryInput --> NemotronText[Send Prepared Prompt to Nemotron]
    QuestInput --> NemotronText

    NemotronText --> ParseJSON[Parse & Validate Structured AI JSON]
    ParseJSON --> RenderUI[Display Story / Quest in Formatted Cards]

    RenderUI --> WantIllustration{Generate Illustration?}
    WantIllustration -->|Yes| CallFlux[FLUX Generates Masterpiece Illustration]
    CallFlux --> DisplayIllus[Display & Save Illustration Locally]
    DisplayIllus --> ActionMenu
    WantIllustration -->|No| ActionMenu{Select Action}

    ActionMenu -->|Save Project| SaveDB[(Persist in Database)]
    ActionMenu -->|Export| DownloadTXT[Download Plain Text Document]
    ActionMenu -->|Regenerate| NemotronText

    SaveDB --> End([Workflow Completed])
    DownloadTXT --> End
```

---

### 5. Sequence Diagram: Text-to-Story-to-Image Generation

```mermaid
sequenceDiagram
    autonumber
    actor User as Writer
    participant UI as Streamlit Frontend
    participant API as FastAPI Backend
    participant Auth as Security Layer (JWT)
    participant Nemotron as NVIDIA Nemotron API
    participant Flux as NVIDIA FLUX API
    participant DB as MySQL / SQLite

    User->>UI: Enter story details & click "Generate Story"
    UI->>API: POST /api/generate/story (Bearer Token, Payload)
    API->>Auth: Validate JWT
    Auth-->>API: User authenticated (ID=1)
    API->>Nemotron: POST /chat/completions (Structured Prompt)
    Nemotron-->>API: JSON Story Arc & Suggested Image Prompt
    API->>DB: Log GenerationHistory (STORY)
    API-->>UI: Return StoryResponse (JSON)
    UI-->>User: Display Formatted Story Cards

    User->>UI: Click "Generate Illustration"
    UI->>API: POST /api/images/generate (Prompt, Style, Mood)
    API->>Flux: POST /genai/flux-1-dev
    Flux-->>API: Image binary / base64
    API->>API: Save locally to uploads/generated/
    API-->>UI: Return relative image path
    UI-->>User: Display Generated Illustration Preview

    User->>UI: Click "Save Project"
    UI->>API: POST /api/projects (Title, Content, ImagePaths)
    API->>DB: Insert Project & ProjectImages records
    DB-->>API: Project ID Created
    API-->>UI: Return ProjectResponse (ID=101)
    UI-->>User: Show Success Notification
```
