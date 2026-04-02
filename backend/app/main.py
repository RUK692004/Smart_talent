from fastapi import FastAPI
from app.routes.resume_upload import router as upload_router

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Backend is running 🚀"}

app.include_router(upload_router)