import os
from fastapi import HTTPException
from openai import OpenAI
from backend.services.embedding import EmbeddingService
from backend.services.vector_store import vector_store
from backend.services.state import document_store
from backend.services.redis_store import redis_store

USE_MOCK_LLM = os.getenv("USE_MOCK_LLM", "true").lower() == "true"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
embedding_service = EmbeddingService()


def retrieve_context(query: str, top_k: int = 5):
    query_embedding = embedding_service.embed_query(query)
    results = vector_store.search(query_embedding, top_k)

    if not results:
        return None

    return "\n\n".join(
        f"[Source: {r['metadata'].get('source', 'unknown')}]\n{r['text']}"
        for r in results
    )


def mock_llm_response(question: str, context: str) -> str:
    return f"""
[MOCK RESPONSE]

Question:
{question}

Based on retrieved resume and JD context, here is a structured answer:
- Some skills align with the job
- Some gaps exist
- Resume wording can be improved

(Context preview)
{context[:300]}...
"""


def generate_answer(question: str, session_id: str) -> str:
    if not redis_store.is_vector_built(session_id):
        raise HTTPException(
            status_code=400,
            detail="Vector store not built. Upload resume, JD, then build vector store first."
        )

    context = retrieve_context(question)

    if not context:
        return "No relevant context found."

    # ✅ MOCK MODE
    if USE_MOCK_LLM:
        return mock_llm_response(question, context)

    # ✅ REAL LLM MODE
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a senior AI career assistant. "
                    "Answer ONLY using the provided context."
                )
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{question}"
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content
