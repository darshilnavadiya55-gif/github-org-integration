# GitHub Organization Integration - FastAPI Starter

A production-minded starter backend for ingesting GitHub organization events and serving analytics.

## Features
- FastAPI app with structured routers
- GitHub OAuth 2.0 authorization flow skeleton
- GitHub webhook endpoint with HMAC SHA-256 signature validation
- MongoDB connection via Motor
- Basic analytics endpoint for org overview

## Project Structure
- `app/main.py` - app initialization and route registration
- `app/core/` - settings and shared security helpers
- `app/db/` - MongoDB client and dependency
- `app/api/` - auth/webhook/analytics endpoints
- `app/services/` - GitHub API client logic
- `app/models/` - pydantic request/response models

## Setup
1. Create and activate virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create `.env` from `.env.example` and fill credentials.
4. Run API:
   ```bash
   uvicorn main:app --reload
   ```

## Key Routes
- `GET /health`
- `GET /auth/github/login`
- `GET /auth/github/callback`
- `POST /webhooks/github`
- `GET /analytics/org/{org_name}/overview`

## Notes
- For local webhook testing, use ngrok and set GitHub webhook target to your public URL.
- Token encryption/storage is scaffolded; replace with secure KMS-backed solution before production.
