from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import traceback

print(">>> importing upload_router")
from app.routes.resume_upload import router as upload_router
print(">>> importing resume_router")
from app.routes.resume import router as resume_router
print(">>> importing jd_router")
from app.routes.jd import router as jd_router
print(">>> importing ranking_router")
from app.routes.ranking import router as ranking_router

app = FastAPI()

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    traceback.print_exc()
    print(f"GLOBAL ERROR: {str(exc)}")
    return JSONResponse(status_code=500, content={"detail": str(exc)})

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