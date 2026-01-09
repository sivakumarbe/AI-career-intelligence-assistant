import re

def normalize_skills(skills):
    return set([s.lower().strip() for s in skills])


def skill_gap_analysis(resume_skills, jd_skills):
    resume_set = normalize_skills(resume_skills)
    jd_set = normalize_skills(jd_skills)

    matched = resume_set.intersection(jd_set)
    missing = jd_set - resume_set

    return {
        "matched_skills": list(matched),
        "missing_skills": list(missing),
        "match_percentage": round(len(matched) / max(len(jd_set), 1) * 100, 2)
    }



# You can expand this list over time
KNOWN_SKILLS = {
    "python", "sql", "machine learning", "deep learning", "nlp",
    "fastapi", "flask", "docker", "aws", "azure", "git",
    "pytorch", "tensorflow", "llm", "rag", "opencv",
    "pandas", "numpy", "scikit-learn", "redis", "faiss"

}

def extract_skills(text: str) -> set:
    text = text.lower()
    found_skills = set()

    for skill in KNOWN_SKILLS:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            found_skills.add(skill)

    return found_skills

def calculate_skill_match(resume_text: str, jd_text: str) -> dict:
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    matched_skills = resume_skills.intersection(jd_skills)

    if len(jd_skills) == 0:
        match_percentage = 0.0
    else:
        match_percentage = round(
            (len(matched_skills) / len(jd_skills)) * 100, 2
        )

    return {
        "match_percentage": match_percentage,
        "matched_skills": sorted(list(matched_skills)),
        "missing_skills": sorted(list(jd_skills - matched_skills)),
        "resume_skills": sorted(list(resume_skills)),
        "jd_skills": sorted(list(jd_skills))
    }

