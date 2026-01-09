from fastapi import APIRouter, HTTPException, Header
from backend.services.rag_engine import retrieve_context
from backend.services.redis_store import redis_store
from backend.services.feature_prompts import (
    skill_gap_prompt,
    rewrite_resume_prompt,
    interview_questions_prompt,
    ats_keywords_prompt,
)
from backend.services.rag_engine import client
from backend.services.state import document_store
from backend.services.skill_matcher import calculate_skill_match
from backend.services.redis_store import redis_store

router = APIRouter()

def llm_call(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content


@router.post("/skill_gap")
def skill_gap(session_id: str = Header(..., alias="X-Session-ID")):
    resume_text = redis_store.get_resume(session_id)
    jd_text = redis_store.get_jd(session_id)

    if not resume_text or not jd_text:
        raise HTTPException(status_code=400, detail="Resume or JD missing")

    result = calculate_skill_match(resume_text, jd_text)

    return {
        "result": {
            "skill_match_percentage": result["match_percentage"],
            "matched_skills": result["matched_skills"],
            "missing_skills": result["missing_skills"]
        }
    }

@router.post("/rewrite_resume")
def rewrite_resume(session_id: str = Header(..., alias="X-Session-ID")):
    if not redis_store.is_vector_built(session_id):
        raise HTTPException(400, "Build vector store first")

    context = retrieve_context("resume experience and job requirements")
    return {"result": llm_call(rewrite_resume_prompt(context))}


@router.post("/interview_questions")
def interview_questions(session_id: str = Header(..., alias="X-Session-ID")):
    if not redis_store.is_vector_built(session_id):
        raise HTTPException(400, "Build vector store first")

    context = retrieve_context("interview relevant skills and projects")
    return {"result": llm_call(interview_questions_prompt(context))}


@router.post("/ats_keywords")
def ats_keywords(session_id: str = Header(..., alias="X-Session-ID")):
    if not redis_store.is_vector_built(session_id):
        raise HTTPException(400, "Build vector store first")

    context = retrieve_context("important skills and tools")
    return {"result": llm_call(ats_keywords_prompt(context))}

