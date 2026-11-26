import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from backend.config import settings

logger = logging.getLogger("narrative_studio.database")

# Build database engine with resilient fallback
db_url = settings.DATABASE_URL

if db_url.startswith("sqlite"):
    engine = create_engine(
        db_url,
        connect_args={"check_same_thread": False}
    )
elif db_url.startswith("mysql"):
    try:
        # Test connection with short timeout to detect if MySQL is running
        temp_engine = create_engine(db_url, pool_pre_ping=True, connect_args={"connect_timeout": 3})
        with temp_engine.connect() as conn:
            pass
        engine = temp_engine
        logger.info("Connected successfully to MySQL database.")
    except Exception as e:
        logger.warning(
            f"Could not connect to MySQL at {db_url} ({e}). "
            "Falling back to local SQLite database (narrative_studio.db) for development."
        )
        engine = create_engine(
            "sqlite:///./narrative_studio.db",
            connect_args={"check_same_thread": False}
        )
else:
    engine = create_engine(db_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency for obtaining a SQLAlchemy session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
