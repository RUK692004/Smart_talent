from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil
import uuid

from app.services.resume_pipeline import process_resume
from app.services.resume_service import save_resume_to_db

router = APIRouter()

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".jpg", ".jpeg", ".png"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def is_allowed_file(filename: str) -> bool:
    _, ext = os.path.splitext(filename.lower())
    return ext in ALLOWED_EXTENSIONS


@router.post("/upload-resume")
def upload_resume(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    if not is_allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="Unsupported file type")

    unique_filename = f"{uuid.uuid4().hex}_{file.filename}"
    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)

    try:
        print("ROUTE: request received")

        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        print("ROUTE: file saved")

        # Run extraction + parsing pipeline
        result = process_resume(file_path, file.filename)
        print("ROUTE: pipeline finished")

        if result.get("status") != "success":
            raise HTTPException(
                status_code=500,
                detail=result.get("message", "Resume processing failed")
            )

        raw_text = result.get("raw_text", "")
        structured_data = result.get("structured_data", {}) or {}

        # Try to get job role if present
        job_role = (
            structured_data.get("job_role")
            or structured_data.get("target_role")
            or structured_data.get("predicted_role")
        )

        # Save to database
        saved_resume = save_resume_to_db(
            filename=file.filename,
            raw_text=raw_text,
            parsed_data=structured_data,
            job_role=job_role
        )
        print("ROUTE: saved to database")

        return {
            "filename": file.filename,
            "saved_as": unique_filename,
            "status": result.get("status"),
            "message": result.get("message"),
            "resume_id": saved_resume.id,
            "extraction_method": result.get("extraction_method"),
            "raw_text": raw_text,
            "cleaned_text": result.get("cleaned_text"),
            "structured_data": structured_data
        }

    except HTTPException:
        raise

    except Exception as e:
        print("ROUTE ERROR:", str(e))
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")