import os
import uuid
import shutil

from fastapi import APIRouter, UploadFile, File, Header, HTTPException
from pydantic import BaseModel

from backend.services.text_extraction import extract_text
from backend.services.preprocessing import clean_text
from backend.services.redis_store import redis_store

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "backend", "data", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ======================================================
# 1️⃣ Upload Resume via FILE
# ======================================================
@router.post("/upload_resume")
async def upload_resume(
    file: UploadFile = File(...),
    session_id: str = Header(..., alias="X-Session-ID")
):
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    raw_text = extract_text(file_path)
    cleaned_text = clean_text(raw_text)

    if not cleaned_text.strip():
        raise HTTPException(status_code=400, detail="Extracted resume text is empty")

    redis_store.store_resume(session_id, cleaned_text)

    return {
        "message": "Resume uploaded successfully (file)",
        "session_id": session_id,
        "characters": len(cleaned_text)
    }


# ======================================================
# 2️⃣ Upload Resume via PASTED TEXT
# ======================================================
class ResumeTextRequest(BaseModel):
    resume_text: str


@router.post("/upload_resume_text")
async def upload_resume_text(
    payload: ResumeTextRequest,
    session_id: str = Header(..., alias="X-Session-ID")
):
    if not payload.resume_text or not payload.resume_text.strip():
        raise HTTPException(status_code=400, detail="Resume text is empty")

    cleaned_text = clean_text(payload.resume_text)

    if not cleaned_text.strip():
        raise HTTPException(status_code=400, detail="Cleaned resume text is empty")

    redis_store.store_resume(session_id, cleaned_text)

    return {
        "message": "Resume uploaded successfully (text)",
        "session_id": session_id,
        "characters": len(cleaned_text)
    }
