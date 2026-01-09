import requests
from config import BACKEND_URL

def _headers(session_id):
    return {"X-Session-ID": session_id}

def upload_resume(file, session_id):
    return requests.post(
        f"{BACKEND_URL}/upload_resume",
        files={"file": file},
        headers={"X-Session-ID": session_id}
    )


def upload_jd(file, session_id):
    return requests.post(
        f"{BACKEND_URL}/upload_jd",
        files={"file": file},
        headers={"X-Session-ID": session_id}
    )


# ===============================
# NEW: Upload Resume via TEXT
# ===============================
def upload_resume_text(resume_text, session_id):
    return requests.post(
        f"{BACKEND_URL}/upload_resume_text",
        json={"resume_text": resume_text},
        headers={"X-Session-ID": session_id}
    )


# ===============================
# NEW: Upload JD via TEXT
# ===============================
def upload_jd_text(jd_text, session_id):
    return requests.post(
        f"{BACKEND_URL}/upload_jd_text",
        json={"jd_text": jd_text},
        headers={"X-Session-ID": session_id}
    )

def build_vector_store(session_id):
    return requests.post(
        f"{BACKEND_URL}/build_vector_store",
        headers=_headers(session_id)
    )

def call_feature(endpoint, session_id):
    return requests.post(
        f"{BACKEND_URL}/{endpoint}",
        headers=_headers(session_id)
    )

def rag_query(question, session_id):
    return requests.post(
        f"{BACKEND_URL}/rag_query",
        json={"question": question},
        headers={"X-Session-ID": session_id}
    )

