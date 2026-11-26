from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base


class GenerationHistory(Base):
    __tablename__ = "generation_history"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="SET NULL"), nullable=True, index=True)
    operation_type = Column(String(50), nullable=False, index=True)  # 'STORY', 'QUEST', 'IMAGE_ANALYSIS', 'IMAGE_GENERATION'
    model_name = Column(String(150), nullable=False)
    input_prompt = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship
    project = relationship("Project", back_populates="generation_history")
