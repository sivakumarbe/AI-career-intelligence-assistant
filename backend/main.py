from fastapi import FastAPI
from backend.api.resume import router as resume_router
from backend.api.jd import router as jd_router
from backend.api.vector_api import router as vector_router
from backend.api.rag_api import router as rag_router
from backend.api.features_api import router as features_router



from dotenv import load_dotenv
load_dotenv()



app = FastAPI(title="AI Career Intelligence Assistant")

app.include_router(resume_router)
app.include_router(jd_router)
app.include_router(vector_router)
app.include_router(rag_router)
app.include_router(features_router)


@app.get("/")
def health_check():
    return {"status": "API running"}
