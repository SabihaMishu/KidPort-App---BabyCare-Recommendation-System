# KidPort — BabyCare Recommendation System

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](./LICENSE)
[![Repo Size](https://img.shields.io/github/repo-size/SabihaMishu/KidPort-App---BabyCare-Recommendation-System)](https://github.com/SabihaMishu/KidPort-App---BabyCare-Recommendation-System)

A baby-care recommendation and growth-tracking platform that combines a Django-based admin and authentication backend with a FastAPI AI microservice to deliver evidence-based recommendations, milestone checks, and curated content for parents and caregivers.

Table of contents
- Project overview
- Architecture & stack
- What’s included
- Quick start (development)
- Running the services
- API examples
- Dataset & data files
- Contribution & development notes
- License & contact

What this is
-------------
KidPort provides an integrated backend for baby-care recommendations: a Django-based admin/auth system (for user, role, and invite management) and a separate FastAPI AI backend (for recommendation, analysis, and lightweight AI endpoints). It bundles datasets used for model development and demonstration.

Stack
-----
- Language(s): Python (100%)
- Framework / runtime:
  - Django (admin, authentication, data models)
  - FastAPI (AI microservice, API surface)
- Notable libraries (from repo requirements):
  - fastapi / uvicorn (API server)
  - django (admin + core backend)
  - sqlalchemy (if present in AI backend DB layer)
  - sqlite (kidport.db included)
  - common ML/data libs you might add (pandas, scikit-learn, PyTorch/TF as needed)

