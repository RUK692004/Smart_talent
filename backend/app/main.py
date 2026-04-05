from fastapi import FastAPI
from app.routes.resume_upload import router as upload_router
from app.routes.resume import router as resume_router
from app.routes.jd import router as jd_router
from app.routes.ranking import router as ranking_router

app = FastAPI()

app.include_router(upload_router)
app.include_router(resume_router)
app.include_router(jd_router)
app.include_router(ranking_router)

@app.get("/")
def root():
    return {"message": "Backend is running 🚀"}