import os

from app.services.file_parser import extract_text
from app.services.text_cleaner import clean_ocr_text, clean_docx_text
from app.services.resume_extractor import extract_resume_data


def process_resume(file_path: str, filename: str) -> dict:
    _, ext = os.path.splitext(filename.lower())

    # Step 1: extract raw text
    extracted_text = extract_text(file_path)

    # Step 2: clean text based on file type
    if ext in [".jpg", ".jpeg", ".png"]:
        cleaned_text = clean_ocr_text(extracted_text)
    else:
        cleaned_text = clean_docx_text(extracted_text)

    # Step 3: convert cleaned text into structured data
    structured_data = extract_resume_data(cleaned_text)

    return {
        "raw_text": extracted_text,
        "cleaned_text": cleaned_text,
        "structured_data": structured_data
    }