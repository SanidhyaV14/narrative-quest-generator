import logging
from backend.database import Base, engine, SessionLocal
from backend.models import User, Project, ProjectImage, GenerationHistory, ProjectFeedback
from backend.utils.security import hash_password

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("init_db")


def init_database():
    """Initializes tables and seeds default user if none exists."""
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Tables created successfully.")

    # Seed demo user
    db = SessionLocal()
    try:
        demo_user = db.query(User).filter(User.email == "demo@narrativestudio.ai").first()
        if not demo_user:
            logger.info("Seeding demo user (demo@narrativestudio.ai)...")
            user = User(
                username="demo_writer",
                email="demo@narrativestudio.ai",
                password_hash=hash_password("password123")
            )
            db.add(user)
            db.commit()
            logger.info("Demo user seeded.")
        else:
            logger.info("Demo user already exists.")
    except Exception as e:
        logger.error(f"Error seeding demo user: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_database()
