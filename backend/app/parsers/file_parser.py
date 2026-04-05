import os
import re
import tempfile
from typing import List

import pdfplumber
import pytesseract
from docx2pdf import convert

from app.preprocess.image_preprocessor import preprocess_image_for_ocr

# ---------- Configuration ----------
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

SUPPORTED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}


# ---------- Helpers ----------
def join_non_empty(lines: List[str]) -> str:
    return "\n".join(line.strip() for line in lines if line and line.strip()).strip()


# ---------- Main Entry ----------
def extract_text(file_path: str) -> str:
    _, ext = os.path.splitext(file_path.lower())

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    elif ext in SUPPORTED_IMAGE_EXTENSIONS:
        return extract_text_from_image(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")


# ---------- PDF Extraction ----------
def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from text-based PDF files.
    """
    try:
        extracted_lines = []

        with pdfplumber.open(file_path) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                text = page.extract_text()
                if text:
                    extracted_lines.append(text)
                else:
                    print(f"FILE_PARSER: no text found on PDF page {page_number}")

        final_text = join_non_empty(extracted_lines)

        if not final_text:
            raise Exception("No readable text found in PDF.")

        return final_text

    except Exception as e:
        raise Exception(f"PDF extraction failed: {str(e)}")


# ---------- DOCX Extraction ----------
def extract_text_from_docx(file_path: str) -> str:
    """
    Convert DOCX to PDF, then use PDF extraction.
    This is more reliable for resumes with complex layouts.
    """
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            pdf_path = os.path.join(temp_dir, "converted_resume.pdf")
            convert(file_path, pdf_path)
            return extract_text_from_pdf(pdf_path)

    except Exception as e:
        raise Exception(f"DOCX to PDF conversion failed: {str(e)}")


# ---------- OCR Result Selection ----------
def choose_best_ocr(text1: str, text2: str) -> str:
    """
    Choose the better OCR result based on simple heuristics.
    """
    def score(text: str) -> int:
        score = 0

        if re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text):
            score += 5

        if re.search(r"(\+?\d[\d\s\-]{8,}\d)", text):
            score += 3

        keywords = [
            "experience", "education", "skills",
            "projects", "profile", "summary"
        ]

        for kw in keywords:
            if kw in text.lower():
                score += 2

        garbage = len(re.findall(r"[^a-zA-Z0-9\s.,\-@]", text))
        score -= garbage // 50

        return score

    score1 = score(text1)
    score2 = score(text2)

    print(f"OCR SCORE psm6: {score1}")
    print(f"OCR SCORE psm11: {score2}")

    return text1 if score1 >= score2 else text2


# ---------- Image Extraction ----------
def extract_text_from_image(file_path: str) -> str:
    """
    Run OCR with multiple PSM modes and choose the best result.
    """
    try:
        print("FILE_PARSER: preprocessing image")
        processed_image = preprocess_image_for_ocr(file_path)

        print("FILE_PARSER: running OCR (psm 6)")
        text_psm6 = pytesseract.image_to_string(
            processed_image,
            config="--oem 3 --psm 6"
        )

        print("FILE_PARSER: running OCR (psm 11)")
        text_psm11 = pytesseract.image_to_string(
            processed_image,
            config="--oem 3 --psm 11"
        )

        best_text = choose_best_ocr(text_psm6, text_psm11)
        final_text = best_text.strip()

        if not final_text:
            raise Exception("No readable text found in image.")

        return final_text

    except Exception as e:
        raise Exception(f"OCR failed: {str(e)}")