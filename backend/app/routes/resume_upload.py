from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil
from app.services.file_parser import extract_text

router = APIRouter()

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".jpg", ".jpeg", ".png"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def is_allowed_file(filename: str) -> bool:
    _, ext = os.path.splitext(filename.lower())
    return ext in ALLOWED_EXTENSIONS

@router.post("/upload-resume")
def upload_resume(file: UploadFile = File(...)):
    if not is_allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="Unsupported file type")

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        extracted_text = extract_text(file_path)

        return {
            "filename": file.filename,
            "status": "uploaded",
            "extracted_text": extracted_text
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))