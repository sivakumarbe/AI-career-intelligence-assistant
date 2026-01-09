from fastapi import APIRouter, HTTPException, Header

from backend.services.rag_engine import generate_answer
from backend.services.redis_store import redis_store

router = APIRouter()


@router.post("/rag_query")
def rag_query(
    payload: dict,
    session_id: str = Header(..., alias="X-Session-ID")
):
    if not redis_store.is_vector_built(session_id):
        raise HTTPException(
            status_code=400,
            detail="Vector store not built. Upload resume, JD, then build vector store first."
        )

    question = payload.get("question", "").strip()
    if not question:
        raise HTTPException(400, "Question is required")

    answer = generate_answer(question, session_id)

    return {
        "session_id": session_id,
        "question": question,
        "answer": answer
    }
