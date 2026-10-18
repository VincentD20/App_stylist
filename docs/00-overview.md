# AI Stylist: Overview

## What it is
A personal web app that digitizes your wardrobe from photos and suggests
outfits by weather and occasion. Clothing `type` and `color` are detected
automatically from the uploaded photo; the user reviews and corrects the result.

## Constraints
- Free to run: no payments or monetization
- No community or social features; each user only sees their own data
- Built as a portfolio project, so security, testing and docs are treated as production-grade

## Stack
- **Backend:** Python, FastAPI, SQLAlchemy, Alembic
- **Database:** PostgreSQL (Docker, local dev)
- **Cache / rate limiting:** Redis
- **File storage:** S3-compatible object storage
- **AI:** vision LLM for classification and color-harmony scoring
- **Auth:** JWT (no RBAC, see ADR-002)
- **Frontend (planned):** React + TypeScript

## Dev environment
- FastAPI runs locally (`uvicorn --reload`), Postgres runs in Docker
- Secrets live in `.env` (gitignored); `.env.example` documents required variables
- FastAPI moves into Docker when CI/CD and deployment are set up

## Project roadmap
1. AI Stylist (this project): computer vision classification, matching, LLM scoring
2. Nutrition / recipe AI: constraint-based recipe scoring
3. Mood-based movie / show matcher: embeddings, no social layer
4. Calisthenics form analyzer: pose estimation, rep counting
