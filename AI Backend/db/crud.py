from sqlalchemy.orm import Session
from . import models

def create_child_log(db: Session, child_id: str, child_name: str, age_months: int, content: str, structured_data: dict, pattern: str = None, recommendation: str = None):
    db_log = models.ChildLog(
        child_id=child_id,
        child_name=child_name,
        age_months=age_months,
        content=content,
        language_score=structured_data.get("language"),
        motor_score=structured_data.get("motor"),
        social_score=structured_data.get("social"),
        cognitive_score=structured_data.get("cognitive"),
        mood=structured_data.get("mood"),
        note=structured_data.get("note"),
        pattern=pattern,
        recommendation=recommendation
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_child_logs(db: Session, child_id: str, limit: int = 7):
    return db.query(models.ChildLog).filter(models.ChildLog.child_id == child_id).order_by(models.ChildLog.created_at.desc()).limit(limit).all()
