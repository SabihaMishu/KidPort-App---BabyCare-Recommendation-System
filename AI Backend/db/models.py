from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .database import Base

class ChildLog(Base):
    __tablename__ = "child_logs"

    id = Column(Integer, primary_key=True, index=True)
    child_id = Column(String, index=True)
    child_name = Column(String, nullable=True)
    age_months = Column(Integer)
    content = Column(String)
    
    # AI Analysis fields
    language_score = Column(Float)
    motor_score = Column(Float)
    social_score = Column(Float)
    cognitive_score = Column(Float)
    mood = Column(String)
    note = Column(String, nullable=True)
    
    # Pattern & Recommendation
    pattern = Column(String, nullable=True)
    recommendation = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
