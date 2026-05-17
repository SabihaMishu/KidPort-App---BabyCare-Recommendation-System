from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from pydantic import BaseModel
from sqlalchemy.orm import Session
import os
import shutil

from db import models
from db.database import engine
from routes import analyze

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="KIDport AI 🚀")

# Include routes
app.include_router(analyze.router, prefix="/api", tags=["analyze"])

@app.get("/")
def root():
    return {"message": "KIDport AI running 🚀"}
