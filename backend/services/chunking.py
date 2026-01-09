import spacy
from typing import List, Dict

nlp = spacy.load("en_core_web_sm")

MAX_TOKENS = 450 


def estimate_tokens(text: str) -> int:

    return len(text.split())


def split_by_sentences(text: str) -> List[str]:
    doc = nlp(text)
    return [sent.text.strip() for sent in doc.sents]


def create_chunks(
    text: str,
    source: str,
    section: str
) -> List[Dict]:

    sentences = split_by_sentences(text)
    chunks = []

    current_chunk = ""
    current_tokens = 0

    for sent in sentences:
        sent_tokens = estimate_tokens(sent)

        if current_tokens + sent_tokens <= MAX_TOKENS:
            current_chunk += " " + sent
            current_tokens += sent_tokens
        else:
            chunks.append({
                "text": current_chunk.strip(),
                "metadata": {
                    "source": source,
                    "section": section,
                    "tokens": current_tokens
                }
            })
            current_chunk = sent
            current_tokens = sent_tokens

    if current_chunk:
        chunks.append({
            "text": current_chunk.strip(),
            "metadata": {
                "source": source,
                "section": section,
                "tokens": current_tokens
            }
        })

    return chunks

def build_resume_chunks(resume_text: str):
    return (
        create_chunks(resume_text, source="resume", section="general")
    )


def build_jd_chunks(jd_text: str):
    return (
        create_chunks(jd_text, source="jd", section="general")
    )
