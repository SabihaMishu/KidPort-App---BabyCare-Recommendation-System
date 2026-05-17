import os
import django

# 1. Initialize Django BEFORE importing any models or routers
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.wsgi import WSGIMiddleware
from django.core.wsgi import get_wsgi_application

from app.api.auth import router as auth_router
from app.api.invitations import router as invite_router

# Initialize FastAPI App
app = FastAPI(
    title="KidPort AI Backend",
    description="Authentication and Role-Based Invitation System (Django + FastAPI)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware for Frontend Integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(auth_router, prefix="/api")
app.include_router(invite_router, prefix="/api")

@app.get("/", tags=["Health"])
def health_check():
    return {
        "status": "active",
        "message": "KidPort AI Backend is running smoothly",
        "docs": "/docs",
        "frameworks": ["Django 5.0", "FastAPI"]
    }

# Mount Django WSGI application to serve Django Admin dashboard
# This lets us access the Django Admin panel on the same port at: http://localhost:8000/django/admin/
django_wsgi_app = get_wsgi_application()
app.mount("/django", WSGIMiddleware(django_wsgi_app))
