import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.config import settings
from backend.database import engine, Base
from backend.routes import auth, projects, feedback, generation, images

# Ensure database tables exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Narrative Studio API",
    description="Backend API for Narrative Studio - A Multimodal AI-Powered Story and Game Quest Generator",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for Streamlit and local frontend interactions
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount local uploads directory as static route for frontend image previews
os.makedirs("uploads/references", exist_ok=True)
os.makedirs("uploads/generated", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include API Routers
app.include_router(auth.router, prefix="/api")
app.include_router(projects.router, prefix="/api")
app.include_router(feedback.router, prefix="/api")
app.include_router(generation.router, prefix="/api")
app.include_router(images.router, prefix="/api")


@app.get("/api/health", tags=["Health"])
def health_check():
    """Health check endpoint to verify backend status."""
    return {
        "status": "online",
        "service": "Narrative Studio API",
        "version": "1.0.0",
        "database": settings.DATABASE_URL.split("://")[0]
    }
