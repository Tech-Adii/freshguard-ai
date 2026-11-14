import os
import json
import uuid
import time
from pathlib import Path
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from src.config import settings
from src.models.schemas import VerificationRequest, VerificationReport
from src.core.pipeline import pipeline
from src.core.gateway import gateway
from src.core import db

app = FastAPI(
    title="FreshGuard AI — Fact Verification Engine",
    description="Enterprise verification layer that audits AI outputs against live web consensus.",
    version="2.1.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = Path(__file__).parent / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)

class GoogleAuthRequest(BaseModel):
    email: str
    name: str
    picture: Optional[str] = ""
    credential: Optional[str] = None

class AuthResponse(BaseModel):
    token: str
    user_id: str
    name: str
    email: str
    picture: Optional[str] = ""

class VerifyWithUserRequest(VerificationRequest):
    user_id: Optional[str] = "user_demo"

@app.get("/api/status")
async def get_status():
    bifrost_active = gateway.is_bifrost_alive()
    return {
        "status": "operational",
        "service": "FreshGuard AI",
        "tavily_connected": bool(settings.TAVILY_API_KEY),
        "gateway_active": True,
        "provider": "Bifrost AI Gateway (Maxim AI)" if bifrost_active else "Google Gemini 3.5 (Direct/Bifrost-Ready)",
        "model": settings.GEMINI_MODEL,
        "version": "2.1.0"
    }

# Google Auth Endpoint
@app.post("/api/auth/google", response_model=AuthResponse)
async def google_auth(req: GoogleAuthRequest):
    """Handles Google OAuth Sign-in & Registration."""
    email = req.email.strip().lower()
    name = req.name.strip() or email.split("@")[0].capitalize()
    picture = req.picture or f"https://api.dicebear.com/7.x/bottts/svg?seed={email}"
    
    user = db.get_or_create_google_user(email=email, name=name, picture=picture)
    
    return AuthResponse(
        token=f"tok_{user['id']}",
        user_id=user["id"],
        name=user["name"],
        email=user["email"],
        picture=user["picture"]
    )

# Verification Endpoint with Auto-History
@app.post("/api/verify", response_model=VerificationReport)
async def verify_text(request: VerifyWithUserRequest):
    if not request.text or len(request.text.strip()) < 5:
        raise HTTPException(status_code=400, detail="Input text must be at least 5 characters.")
    
    try:
        report = await pipeline.run(request)
        user_id = request.user_id or "user_demo"
        db.save_history_item(user_id, report.model_dump())
        return report
    except Exception as e:
        print(f"[API] Error running verification: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# History Endpoints
@app.get("/api/history")
async def get_history(user_id: str = "user_demo"):
    return db.get_user_history(user_id)

@app.get("/api/history/{history_id}")
async def get_history_detail(history_id: str):
    detail = db.get_history_detail(history_id)
    if not detail:
        raise HTTPException(status_code=404, detail="History record not found.")
    return detail

@app.delete("/api/history/{history_id}")
async def delete_history_item(history_id: str, user_id: str = "user_demo"):
    success = db.delete_history_item(history_id, user_id)
    return {"deleted": success}

@app.delete("/api/history")
async def clear_history(user_id: str = "user_demo"):
    success = db.clear_user_history(user_id)
    return {"cleared": success}

# Mount static frontend
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/")
async def serve_index():
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"message": "FreshGuard AI API is operational."}
