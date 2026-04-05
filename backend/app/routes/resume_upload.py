from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil

from app.services.resume_pipeline import process_resume

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
        print("ROUTE: request received")
        print(f"ROUTE: filename = {file.filename}")
        print(f"ROUTE: file size = {file.size if hasattr(file, 'size') else 'unknown'}")

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        print("ROUTE: file saved")
        print(f"ROUTE: file path = {file_path}")

        result = process_resume(file_path, file.filename)
        print("ROUTE: pipeline finished")

        return {
            "filename": file.filename,
            "status": "uploaded",
            "raw_text": result["raw_text"],
            "cleaned_text": result["cleaned_text"],
            "structured_data": result["structured_data"],
            "debug_info": {
                "extraction_method": result.get("extraction_method"),
                "message": result.get("message", ""),
                "status": result.get("status", ""),
                "file_path": file_path
            }
        }

    except Exception as e:
        print("ROUTE ERROR:", str(e))
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))