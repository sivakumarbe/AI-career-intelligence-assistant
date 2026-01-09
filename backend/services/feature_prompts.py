def skill_gap_prompt(context: str) -> str:
    return f"""
You are a senior technical recruiter.
Using ONLY the context below, explain skill gaps clearly and honestly.

Context:
{context}

Output:
- Matched skills
- Missing skills
- Actionable suggestions
"""


def rewrite_resume_prompt(context: str) -> str:
    return f"""
You are an ATS optimization expert.
Rewrite resume experience bullets to better match the JD.
Use action verbs and measurable impact.
Do NOT add skills not present in context.

Context:
{context}
"""


def interview_questions_prompt(context: str) -> str:
    return f"""
You are a hiring manager.
Generate interview questions strictly based on the skills and experience in context.

Context:
{context}

Include:
- Technical questions
- Project-based questions
- Behavioral questions
"""


def ats_keywords_prompt(context: str) -> str:
    return f"""
You are an ATS system.
Extract important keywords and phrases recruiters will search for.

Context:
{context}

Output a concise keyword list.
"""
