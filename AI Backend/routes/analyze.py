from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
import os
import shutil

from ai.structuring import analyze_input
from ai.image import image_to_text
from ai.voice import voice_to_text
from ai.video import video_to_text
from ai.recommendation import generate_recommendation
from utils.pattern import get_last7_pattern
from utils.kidmilestone import get_kidmilestone
from db import crud
from db.database import get_db

router = APIRouter()

# Function to process analysis for all input types (text, image, voice, video)
def process_analysis_flow(db: Session, child_id: str, child_name: str, age_months: int, final_content: str):
    """
    Common flow for all analysis endpoints.
    """
    # 1. Analyze input content into structured JSON
    structured = analyze_input(final_content)

    # 2. Save to SQLite DB
    crud.create_child_log(db, child_id, child_name, age_months, final_content, structured)

    # 3. Fetch last 7 logs for pattern detection
    last7_logs = crud.get_child_logs(db, child_id, limit=7)
    
    # Convert DB models to list of dicts for pattern detection
    logs_dict = [
        {
            "child_id": log.child_id,
            "age_months": log.age_months,
            "language": log.language_score,
            "motor": log.motor_score,
            "social": log.social_score,
            "cognitive": log.cognitive_score,
            "mood": log.mood
        }
        for log in last7_logs
    ]
    
    # 4. Detect pattern
    pattern = get_last7_pattern(logs_dict)

    # 5. Fetch milestone
    milestone = get_kidmilestone(age_months)

    # 6. Generate recommendation
    recommendation = generate_recommendation(child_name, age_months, milestone, pattern)

    return {
        "status": "success",
        "structured": structured,
        "pattern": pattern,
        "recommendation": recommendation,
        "milestone": milestone
    }

@router.post("/analyze")
async def analyze_text(
    child_id: str = Form(...),
    child_name: str = Form(...),
    age_months: int = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        return process_analysis_flow(db, child_id, child_name, age_months, content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-image")
async def analyze_image(
    child_id: str = Form(...),
    child_name: str = Form(...),
    age_months: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        description = image_to_text(temp_path)
        os.remove(temp_path)
        
        return process_analysis_flow(db, child_id, child_name, age_months, description)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-voice")
async def analyze_voice(
    child_id: str = Form(...),
    child_name: str = Form(...),
    age_months: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        transcription = voice_to_text(temp_path)
        os.remove(temp_path)
        
        return process_analysis_flow(db, child_id, child_name, age_months, transcription)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-video")
async def analyze_video(
    child_id: str = Form(...),
    child_name: str = Form(...),
    age_months: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        description = video_to_text(temp_path)
        os.remove(temp_path)
        
        return process_analysis_flow(db, child_id, child_name, age_months, description)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))