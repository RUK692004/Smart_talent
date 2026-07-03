from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import uuid
import traceback

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
async def upload_resume(file: UploadFile = File(...)):
    print(">>> ROUTE HIT")

    # --- Validation ---
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    if not is_allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="Unsupported file type")

    unique_filename = f"{uuid.uuid4().hex}_{file.filename}"
    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)

    try:
        # --- Save file ---
        print("ROUTE: saving file")
        contents = await file.read()
        with open(file_path, "wb") as buffer:
            buffer.write(contents)
        print(f"ROUTE: file saved → {file_path}")

        # --- Process resume ---
        print("ROUTE: starting pipeline")
        result = process_resume(file_path, file.filename)
        print(f"ROUTE: pipeline finished with status = {result.get('status')}")

        if result.get("status") != "success":
            error_msg = result.get("message", "Resume processing failed")
            print(f"ROUTE: pipeline error → {error_msg}")
            raise HTTPException(status_code=500, detail=error_msg)

        # --- Extract fields ---
        raw_text = result.get("raw_text", "")
        structured_data = result.get("structured_data") or {}

        job_role = (
            structured_data.get("job_role")
            or structured_data.get("target_role")
            or structured_data.get("predicted_role")
        )

        # --- Save to DB ---
        print("ROUTE: saving to database")
        saved_resume = save_resume_to_db(
            filename=file.filename,
            raw_text=raw_text,
            parsed_data=structured_data,
            job_role=job_role,
            file_path=unique_filename
        )
        print(f"ROUTE: saved → resume_id = {saved_resume.id}")

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
        traceback.print_exc()  # full stack trace in terminal
        print(f"ROUTE ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    finally:
        # Clean up saved file if processing failed midway
        if os.path.exists(file_path) and 'saved_resume' not in dir():
            os.remove(file_path)
            print(f"ROUTE: cleaned up file → {file_path}")