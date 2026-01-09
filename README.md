🧠 AI Career Intelligence & Resume–JD Matching Assistant

An AI-powered system that analyzes a candidate’s resume against a job description using Retrieval-Augmented Generation (RAG), deterministic skill matching, and LLM-based explanations.

This project is designed as a real-world AI product, focusing on accuracy, explainability, cost control, and user experience.

🚀 Features

📄 Resume & Job Description input via file upload OR text paste

🔐 Session-aware multi-user architecture (Redis-backed)

🧠 RAG pipeline using FAISS vector store

📊 Deterministic Skill Match Percentage

💬 Context-aware AI Chat over Resume & JD

📉 Skill Gap analysis (matched vs missing skills)

✍️ Resume rewriting aligned to job requirements

🎤 Interview question generation

📊 ATS keyword extraction

🎯 Non-technical, guided UI flow (error-proof)

🛠️ Tech Stack
Backend

FastAPI – REST APIs

Redis – Session & document storage

FAISS – Vector similarity search

OpenAI LLM – Mock / Real toggle

Python, Pydantic

Frontend

Streamlit – Interactive UI & chat experience

🧠 Core Design Principles
1️⃣ Deterministic over Hallucinated Logic

Skill match percentage is rule-based

LLM is not used for calculations

Formula used:

Skill Match % = (Matched Skills / JD Skills) × 100

2️⃣ Explicit RAG Lifecycle

Resume & JD uploaded once per session

Vector store built explicitly by user

No hidden background embedding jobs

Predictable latency & cost control

3️⃣ LLM Used Only Where It Makes Sense

LLMs are used for:

Natural language explanations

Resume rewriting

Interview question generation

Conversational AI chat

LLMs are not used for:

Skill matching logic

Percent calculations

Critical decision metrics

🧩 System Architecture
Streamlit UI
   │
   │  REST API (X-Session-ID)
   ▼
FastAPI Backend
   │
   ├── Redis (Resume, JD, Session)
   │
   ├── FAISS Vector Store
   │
   ├── Skill Extraction & Matching Logic
   │
   └── LLM (Mock / Real)

🔁 Example Workflow

User uploads or pastes Resume & JD

User clicks Prepare AI Analysis

Backend:

Extracts & cleans text

Builds vector store

User explores:

Skill Gap

AI Chat

Resume Rewrite

Interview Questions

ATS Keywords

💬 RAG Chat

Context-aware chat using vector store

Stable chat input (ChatGPT-style UX)

Clear chat support

Session-isolated conversations

🧪 Mock vs Real LLM
Mode	Purpose
Mock	Development, testing, zero cost
Real	Production & demos

Controlled via environment configuration.

▶️ How to Run Locally
1️⃣ Start Redis
redis-server

2️⃣ Start Backend
uvicorn backend.main:app --reload

3️⃣ Start Frontend
streamlit run frontend/app.py

📂 Repository Structure
carrier_ai_assistant/
│
├── backend/
│   ├── api/
│   ├── services/
│   ├── main.py
│
├── frontend/
│   ├── app.py
│   ├── api_client.py
│   ├── session.py
│
├── README.md
├── requirements.txt
└── .gitignore

🔒 Security & Privacy

.env excluded via .gitignore

Uploaded resumes & JDs not committed

Redis session data not persisted to GitHub

No secrets in repository

🎯 Interview-Ready Explanation

“This project combines deterministic skill matching with session-aware RAG. We use LLMs only for language understanding and explanation, ensuring accuracy, transparency, and cost control.”

🚀 Future Enhancements

Skill weighting (core vs optional)

LLM-based skill normalization

Source citations in RAG responses

Downloadable PDF report

Dockerized deployment

Authentication & user accounts

🏁 Final Note

This project is built as a production-style AI system, not a demo:

Clear separation of concerns

Explainable AI decisions

Scalable architecture

Non-technical friendly UX
