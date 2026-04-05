import os
from typing import Dict, Any

from app.parsers.file_parser import extract_text
from app.utils.text_cleaner import clean_ocr_text, clean_docx_text
from app.services.ai_extractor import extract_structured_data_with_ai
from app.services.rule_based_extractor import extract_resume_data
from app.services.validators import validate_resume_data
from app.services.normalizers import normalize_resume_data


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def process_resume(file_path: str, filename: str) -> Dict[str, Any]:
    """
    Main resume processing pipeline.

    Flow:
    1. Extract raw text from file
    2. Clean extracted text
    3. Try AI-based structured extraction
    4. Fallback to rule-based extraction if AI fails
    5. Validate structured data
    6. Normalize structured data
    7. Return final result
    """
    _, ext = os.path.splitext(filename.lower())

    print("PIPELINE: started")

    try:
        extracted_text = extract_text(file_path)
        print("PIPELINE: text extracted")

        if ext in IMAGE_EXTENSIONS:
            cleaned_text = clean_ocr_text(extracted_text)
            print("PIPELINE: OCR text cleaned")
        else:
            cleaned_text = clean_docx_text(extracted_text)
            print("PIPELINE: document text cleaned")

        ai_result = extract_structured_data_with_ai(cleaned_text)

        if ai_result.get("status") == "success":
            structured_data = ai_result.get("structured_data", {})
            extraction_method = "ai"
            print("PIPELINE: AI structured extraction successful")
        else:
            print("PIPELINE: AI extraction failed")
            print("PIPELINE: AI error message =", ai_result.get("message"))
            structured_data = extract_resume_data(cleaned_text)
            extraction_method = "rule_based"

            if not isinstance(structured_data, dict):
                structured_data = {}

            structured_data["raw_text"] = cleaned_text
            print("PIPELINE: rule-based structured extraction completed")

        validation_result = validate_resume_data(structured_data)

        if validation_result.get("status") != "success":
            return {
                "status": "error",
                "message": validation_result.get("message", "Validation failed."),
                "raw_text": extracted_text,
                "cleaned_text": cleaned_text,
                "structured_data": structured_data,
                "extraction_method": extraction_method
            }

        print("PIPELINE: validation completed")

        normalization_result = normalize_resume_data(
            validation_result.get("structured_data", {})
        )

        if normalization_result.get("status") != "success":
            return {
                "status": "error",
                "message": normalization_result.get("message", "Normalization failed."),
                "raw_text": extracted_text,
                "cleaned_text": cleaned_text,
                "structured_data": validation_result.get("structured_data", {}),
                "extraction_method": extraction_method
            }

        print("PIPELINE: normalization completed")
        print("PIPELINE: finished successfully")

        return {
            "status": "success",
            "message": "Resume processed successfully.",
            "raw_text": extracted_text,
            "cleaned_text": cleaned_text,
            "structured_data": normalization_result.get("structured_data", {}),
            "extraction_method": extraction_method
        }

    except Exception as e:
        print(f"PIPELINE ERROR: {str(e)}")
        return {
            "status": "error",
            "message": f"Resume processing failed: {str(e)}",
            "raw_text": "",
            "cleaned_text": "",
            "structured_data": {},
            "extraction_method": None
        }