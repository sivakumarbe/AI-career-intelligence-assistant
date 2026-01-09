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
# 1️⃣ Upload JD via FILE (PDF / DOCX / TXT)
# ======================================================
@router.post("/upload_jd")
async def upload_jd(
    file: UploadFile = File(...),
    session_id: str = Header(..., alias="X-Session-ID")
):
    # Save file
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract & clean text
    raw_text = extract_text(file_path)
    cleaned_text = clean_text(raw_text)

    if not cleaned_text.strip():
        raise HTTPException(status_code=400, detail="Extracted JD text is empty")

    # Store in Redis
    redis_store.store_jd(session_id, cleaned_text)

    return {
        "message": "Job description uploaded successfully (file)",
        "session_id": session_id,
        "characters": len(cleaned_text)
    }


# ======================================================
# 2️⃣ Upload JD via PASTED TEXT
# ======================================================
class JDTextRequest(BaseModel):
    jd_text: str


@router.post("/upload_jd_text")
async def upload_jd_text(
    payload: JDTextRequest,
    session_id: str = Header(..., alias="X-Session-ID")
):
    if not payload.jd_text or not payload.jd_text.strip():
        raise HTTPException(status_code=400, detail="JD text is empty")

    # Clean pasted text (same pipeline)
    cleaned_text = clean_text(payload.jd_text)

    if not cleaned_text.strip():
        raise HTTPException(status_code=400, detail="Cleaned JD text is empty")

    # Store in Redis
    redis_store.store_jd(session_id, cleaned_text)

    return {
        "message": "Job description uploaded successfully (text)",
        "session_id": session_id,
        "characters": len(cleaned_text)
    }
