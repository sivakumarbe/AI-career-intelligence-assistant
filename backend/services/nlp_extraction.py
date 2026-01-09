import re
import spacy

nlp = spacy.load("en_core_web_sm")

# Common tech skills list (expandable)
TECH_SKILLS = {
    "python", "java", "sql", "tensorflow", "pytorch", "fastapi",
    "docker", "kubernetes", "aws", "azure", "gcp",
    "machine learning", "deep learning", "nlp", "rag"
}

def extract_years_of_experience(text: str):
    matches = re.findall(r'(\d+)\+?\s*(years|yrs)', text.lower())
    return list(set([int(m[0]) for m in matches]))


def extract_skills(text: str):
    doc = nlp(text.lower())
    found_skills = set()

    # phrase-based skill detection
    for token in doc:
        if token.text in TECH_SKILLS:
            found_skills.add(token.text)

    # noun chunks (for multi-word skills)
    for chunk in doc.noun_chunks:
        if chunk.text.lower() in TECH_SKILLS:
            found_skills.add(chunk.text.lower())

    return list(found_skills)


def extract_roles(text: str):
    roles = []
    role_patterns = [
        r"data scientist",
        r"machine learning engineer",
        r"ai engineer",
        r"software engineer",
        r"backend developer"
    ]

    text = text.lower()
    for role in role_patterns:
        if role in text:
            roles.append(role)

    return list(set(roles))


def extract_entities(text: str):
    doc = nlp(text)
    orgs = set()
    dates = set()

    for ent in doc.ents:
        if ent.label_ == "ORG":
            orgs.add(ent.text)
        elif ent.label_ == "DATE":
            dates.add(ent.text)

    return {
        "organizations": list(orgs),
        "dates": list(dates)
    }


def extract_resume_insights(text: str):
    return {
        "skills": extract_skills(text),
        "roles": extract_roles(text),
        "years_of_experience": extract_years_of_experience(text),
        "entities": extract_entities(text)
    }
