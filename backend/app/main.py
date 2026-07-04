from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import traceback

print(">>> importing upload_router")
from app.api.upload import router as upload_router
print(">>> importing resume_router")
from app.api.resume import router as resume_router
print(">>> importing jd_router")
from app.api.jd import router as jd_router
print(">>> importing ranking_router")
from app.api.ranking import router as ranking_router

print(">>> importing config")
from app.config.settings import CORS_ORIGINS

print(">>> importing middleware")
from app.middleware.exception_handler import global_exception_handler

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return await global_exception_handler(request, exc)

@app.on_event("startup")
async def startup_event():
    print(">>> STARTUP EVENT FIRED")

app.include_router(upload_router)
app.include_router(resume_router)
app.include_router(jd_router)
app.include_router(ranking_router)

@app.get("/")
def root():
    return {"message": "Backend is running 🚀"}