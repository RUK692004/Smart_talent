import os
from typing import List

import pdfplumber
import pytesseract
from docx import Document
from docx2pdf import convert
from pdf2image import convert_from_path
from PIL import Image
import re



# ---------- Configuration ----------
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH = r"C:\poppler\Library\bin"

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

SUPPORTED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
IMPORTANT_KEYWORDS = ["@", "linkedin", "github", "+91", "email"]

# ---------- LOGIC ----------

def get_top_text(text: str, max_chars: int = 1000) -> str:
    """
    Return only the top portion of the extracted text.
    """
    return text[:max_chars].lower()


def has_phone_number(text: str) -> bool:
    """
    Detect common phone number formats, including Indian numbers.
    """
    phone_pattern = r"(\+91[\s-]?\d{10}|\b\d{10}\b)"
    return re.search(phone_pattern, text) is not None


def has_email(text: str) -> bool:
    """
    Detect whether any email exists.
    """
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    return re.search(email_pattern, text) is not None


def has_profile_links_or_labels(text: str) -> bool:
    """
    Detect LinkedIn/GitHub mention in the top section.
    """
    text = text.lower()
    return "linkedin" in text or "github" in text


def is_top_section_incomplete(text: str) -> bool:
    """
    Strong check for missing candidate identity.
    """
    top_text = get_top_text(text)

    # MUST have at least one strong personal identifier
    has_personal_email = has_email(top_text)
    has_phone = has_phone_number(top_text)

    # Additional signals
    has_links = has_profile_links_or_labels(top_text)
    has_dob = "dob" in top_text

    # STRONG RULE:
    # At least (email OR phone) MUST exist
    # AND at least one supporting signal

    if (has_personal_email or has_phone) and (has_links or has_dob):
        return False  # good extraction

    return True  # incomplete → trigger fallback
# ---------- Main Entry ----------

def extract_text(file_path: str) -> str:
    try:
        _, ext = os.path.splitext(file_path.lower())

        if ext == ".pdf":
            return extract_text_from_pdf(file_path)

        if ext == ".docx":
            return extract_text_from_docx(file_path)

        if ext in SUPPORTED_IMAGE_EXTENSIONS:
            return extract_text_from_image(file_path)

        raise ValueError(f"Unsupported file format: {ext}")

    except Exception as e:
        raise Exception(f"Error processing file '{file_path}': {str(e)}")


# ---------- Utility Helpers ----------
def join_non_empty(lines: List[str]) -> str:
    return "\n".join(line.strip() for line in lines if line and line.strip()).strip()


def count_important_keywords(text: str) -> int:
    text_lower = text.lower()
    return sum(1 for keyword in IMPORTANT_KEYWORDS if keyword in text_lower)


def is_text_incomplete(text: str, min_length: int = 200, min_keyword_hits: int = 2) -> bool:
    return len(text.strip()) < min_length or count_important_keywords(text) < min_keyword_hits


# ---------- PDF Extraction ----------
def extract_text_from_pdf(file_path: str) -> str:
    try:
        extracted_lines = []

        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    extracted_lines.append(text)

        return join_non_empty(extracted_lines)

    except Exception as e:
        raise Exception(f"PDF extraction failed: {str(e)}")


def extract_text_from_pdf_ocr(file_path: str) -> str:
    try:
        images = convert_from_path(file_path, poppler_path=POPPLER_PATH)
        extracted_lines = []

        for image in images:
            text = pytesseract.image_to_string(image)
            if text:
                extracted_lines.append(text)

        return join_non_empty(extracted_lines)

    except Exception as e:
        raise Exception(f"PDF OCR extraction failed: {str(e)}")


# ---------- DOCX Extraction ----------
def convert_docx_to_pdf(file_path: str) -> str:
    try:
        pdf_path = file_path.rsplit(".", 1)[0] + ".pdf"
        convert(file_path, pdf_path)
        return pdf_path

    except Exception as e:
        raise Exception(f"DOCX to PDF conversion failed: {str(e)}")


def extract_text_from_docx_direct(file_path: str) -> str:
    try:
        doc = Document(file_path)
        extracted_lines = []

        # Paragraphs
        for para in doc.paragraphs:
            if para.text.strip():
                extracted_lines.append(para.text)

        # Tables
        for table in doc.tables:
            for row in table.rows:
                row_data = []
                for cell in row.cells:
                    cell_text = cell.text.strip()
                    if cell_text:
                        row_data.append(cell_text)

                if row_data:
                    extracted_lines.append(" | ".join(row_data))

        # Headers & Footers
        for section in doc.sections:
            for para in section.header.paragraphs:
                if para.text.strip():
                    extracted_lines.append(para.text)

            for para in section.footer.paragraphs:
                if para.text.strip():
                    extracted_lines.append(para.text)

        return join_non_empty(extracted_lines)

    except Exception as e:
        raise Exception(f"DOCX direct extraction failed: {str(e)}")


def extract_text_from_docx(file_path: str) -> str:
    try:
        direct_text = extract_text_from_docx_direct(file_path)

        if not is_top_section_incomplete(direct_text):
            print("✔ Using direct DOCX extraction")
            return direct_text

        print("⚠️ Direct extraction incomplete → trying PDF")

        pdf_path = convert_docx_to_pdf(file_path)
        pdf_text = extract_text_from_pdf(pdf_path)

        if not is_top_section_incomplete(pdf_text):
            print("✔ Using DOCX -> PDF extraction")
            return pdf_text

        print("🔥 Falling back to OCR extraction")

        return extract_text_from_pdf_ocr(pdf_path)

    except Exception as e:
        raise Exception(f"DOCX processing failed: {str(e)}")


# ---------- Image Extraction ----------
def extract_text_from_image(file_path: str) -> str:
    try:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        return text.strip()

    except Exception as e:
        raise Exception(f"Image OCR extraction failed: {str(e)}")