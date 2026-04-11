from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .session import Base

class AnalysisHistory(Base):
    __tablename__ = "analysis_history"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    job_description = Column(String)
    ats_score = Column(Float)
    matched_skills = Column(String) # Stored as JSON or comma-separated string
    missing_skills = Column(String) # Stored as JSON or comma-separated string
    created_at = Column(DateTime, default=datetime.utcnow)
