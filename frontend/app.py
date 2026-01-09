import streamlit as st

from session import get_session_id
from api_client import (
    upload_resume,
    upload_jd,
    build_vector_store,
    call_feature,
    rag_query,
    upload_resume_text,
    upload_jd_text
)

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(
    page_title="AI Career Intelligence",
    layout="wide"
)

# --------------------------------------------------
# Session
# --------------------------------------------------
session_id = get_session_id()

# State flags
if "resume_uploaded" not in st.session_state:
    st.session_state.resume_uploaded = False

if "jd_uploaded" not in st.session_state:
    st.session_state.jd_uploaded = False

if "vector_ready" not in st.session_state:
    st.session_state.vector_ready = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.sidebar.title("Session")
st.sidebar.code(session_id)

st.title("🧠 AI Career Intelligence Assistant")
st.caption("Upload or paste your resume and job description to get AI-powered insights")

# --------------------------------------------------
# Helper
# --------------------------------------------------
def handle_response(res, success_msg="Success"):
    try:
        data = res.json()
    except Exception:
        st.error("Invalid response from server")
        return False

    if res.status_code == 200:
        st.success(data.get("message", success_msg))
        return True
    else:
        st.error(data.get("detail", "Operation failed"))
        return False

# ==================================================
# STEP 1: Upload / Paste Resume & JD
# ==================================================
st.header("📤 Step 1: Provide Resume & Job Description")

col1, col2 = st.columns(2)

# -------------------- RESUME --------------------
with col1:
    st.subheader("Resume")

    resume_mode = st.radio(
        "Resume input method",
        ["Upload File", "Paste Text"],
        horizontal=True,
        key="resume_mode"
    )

    resume_file = None
    resume_text = None

    if resume_mode == "Upload File":
        resume_file = st.file_uploader(
            "Upload Resume",
            type=["pdf", "docx", "doc", "txt"]
        )
    else:
        resume_text = st.text_area(
            "Paste Resume Text",
            height=250,
            placeholder="Paste your resume content here..."
        )

    if st.button("Upload Resume"):
        with st.spinner("Processing resume..."):
            if resume_mode == "Upload File":
                if not resume_file:
                    st.error("Please upload a resume file")
                else:
                    res = upload_resume(resume_file, session_id)
                    if handle_response(res, "Resume uploaded"):
                        st.session_state.resume_uploaded = True
            else:
                if not resume_text or not resume_text.strip():
                    st.error("Please paste resume text")
                else:
                    res = upload_resume_text(resume_text, session_id)
                    if handle_response(res, "Resume uploaded"):
                        st.session_state.resume_uploaded = True

# -------------------- JD --------------------
with col2:
    st.subheader("Job Description")

    jd_mode = st.radio(
        "Job Description input method",
        ["Upload File", "Paste Text"],
        horizontal=True,
        key="jd_mode"
    )

    jd_file = None
    jd_text = None

    if jd_mode == "Upload File":
        jd_file = st.file_uploader(
            "Upload Job Description",
            type=["pdf", "docx", "doc", "txt"]
        )
    else:
        jd_text = st.text_area(
            "Paste Job Description Text",
            height=250,
            placeholder="Paste the full job description here..."
        )

    if st.button("Upload Job Description"):
        with st.spinner("Processing job description..."):
            if jd_mode == "Upload File":
                if not jd_file:
                    st.error("Please upload a job description file")
                else:
                    res = upload_jd(jd_file, session_id)
                    if handle_response(res, "Job description uploaded"):
                        st.session_state.jd_uploaded = True
            else:
                if not jd_text or not jd_text.strip():
                    st.error("Please paste job description text")
                else:
                    res = upload_jd_text(jd_text, session_id)
                    if handle_response(res, "Job description uploaded"):
                        st.session_state.jd_uploaded = True

# ==================================================
# STEP 2: Prepare AI Analysis
# ==================================================
st.divider()
st.header("⚙️ Step 2: Prepare AI Analysis")

if not st.session_state.resume_uploaded or not st.session_state.jd_uploaded:
    st.warning("Please upload BOTH Resume and Job Description to continue")

can_build_vector = (
    st.session_state.resume_uploaded
    and st.session_state.jd_uploaded
    and not st.session_state.vector_ready
)

if st.button("🚀 Prepare AI Analysis", disabled=not can_build_vector):
    with st.spinner("Analyzing resume and job description..."):
        res = build_vector_store(session_id)
        if handle_response(res, "AI analysis is ready"):
            st.session_state.vector_ready = True

if st.session_state.vector_ready:
    st.success("✅ Analysis ready. You can now explore insights.")

# ==================================================
# STEP 3: Explore AI Insights
# ==================================================
st.divider()
st.header("🧩 Step 3: Explore AI Insights")

tabs = st.tabs([
    "💬 AI Chat",
    "📉 Skill Gap",
    "✍️ Resume Rewrite",
    "🎤 Interview Questions",
    "📊 ATS Keywords"
])

# -------------------- AI CHAT --------------------
with tabs[0]:
    st.subheader("💬 Ask questions about your Resume & Job Description")

    if not st.session_state.vector_ready:
        st.info("Prepare AI analysis to enable chat")
    else:
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()

        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        user_query = st.chat_input("Ask anything about your career fit...")

        if user_query and user_query.strip():
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_query
            })

            with st.spinner("Thinking..."):
                res = rag_query(user_query, session_id)
                answer = (
                    res.json().get("answer")
                    if res.status_code == 200
                    else res.json().get("detail", "Something went wrong")
                )

            st.session_state.chat_history.append({
                "role": "assistant",
                "content": answer
            })

            st.rerun()

# -------------------- FEATURE TABS --------------------
feature_map = [
    ("📉 Skill Gap", "skill_gap"),
    ("✍️ Resume Rewrite", "rewrite_resume"),
    ("🎤 Interview Questions", "interview_questions"),
    ("📊 ATS Keywords", "ats_keywords")
]

for tab, (label, endpoint) in zip(tabs[1:], feature_map):
    with tab:
        st.subheader(label)

        if not st.session_state.vector_ready:
            st.info("Prepare AI analysis to unlock this feature")
            st.button(f"Run {label}", disabled=True)
            continue

        if st.button(f"Run {label}"):
            with st.spinner(f"Running {label.lower()}..."):
                res = call_feature(endpoint, session_id)

                # ✅ STRUCTURED SKILL GAP UI
                if endpoint == "skill_gap" and res.status_code == 200:
                    data = res.json()["result"]

                    st.metric(
                        "Skill Match Percentage",
                        f"{data['skill_match_percentage']}%"
                    )

                    st.divider()

                    st.subheader("✅ Matched Skills")
                    if data["matched_skills"]:
                        cols = st.columns(3)
                        for i, skill in enumerate(data["matched_skills"]):
                            cols[i % 3].success(skill)
                    else:
                        st.warning("No matched skills found")

                    st.subheader("❌ Missing Skills")
                    if data["missing_skills"]:
                        cols = st.columns(3)
                        for i, skill in enumerate(data["missing_skills"]):
                            cols[i % 3].error(skill)
                    else:
                        st.success("No missing skills 🎉")

                elif res.status_code == 200:
                    st.markdown(res.json().get("result", "No output"))

                else:
                    st.error(res.json().get("detail", "Request failed"))
