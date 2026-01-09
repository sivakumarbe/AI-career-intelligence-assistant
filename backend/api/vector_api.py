from fastapi import APIRouter, HTTPException, Header

from backend.services.redis_store import redis_store
from backend.services.embedding import EmbeddingService
from backend.services.vector_store import vector_store
from backend.services.chunking import build_resume_chunks, build_jd_chunks

router = APIRouter()
embedding_service = EmbeddingService()


@router.post("/build_vector_store")
def build_vector_store(session_id: str = Header(..., alias="X-Session-ID")):
    resume_text = redis_store.get_resume(session_id)
    jd_text = redis_store.get_jd(session_id)

    if not resume_text or not jd_text:
        raise HTTPException(
            status_code=400,
            detail="Upload resume and JD before building vector store"
        )

    # Chunking
    resume_chunks = build_resume_chunks(resume_text)
    jd_chunks = build_jd_chunks(jd_text)
    all_chunks = resume_chunks + jd_chunks

    texts = [c["text"] for c in all_chunks]
    metadatas = [c["metadata"] for c in all_chunks]

    # Embeddings
    embeddings = embedding_service.embed_texts(texts)

    # Reset & add
    vector_store.reset()
    vector_store.add(embeddings, texts, metadatas)

    redis_store.mark_vector_built(session_id)

    return {
        "message": "Vector store built successfully",
        "session_id": session_id,
        "total_vectors": len(texts)
    }
