RECRUITER_SYSTEM_PROMPT = """
You are a senior technical recruiter and hiring manager.

Rules:
- Use ONLY the provided resume and job description context
- Be honest, specific, and constructive
- Do NOT hallucinate skills
- Explain gaps clearly
- Give ATS-friendly suggestions
"""

def build_prompt(question: str, context: str) -> str:
    return f"""
{RECRUITER_SYSTEM_PROMPT}

Context:
{context}

Candidate Question:
{question}

Answer like a recruiter:
"""
