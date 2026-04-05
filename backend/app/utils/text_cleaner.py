import re


def clean_text_general(text: str) -> str:
    text = text.replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n+", "\n", text)
    return text.strip()


def clean_ocr_text(text: str) -> str:
    # Normalize weird OCR symbols instead of removing all of them
    text = text.replace("‘*", "•")
    text = text.replace("'*", "•")
    text = text.replace("*", "•")
    text = text.replace("©", "•")
    text = text.replace("°", "•")

    # Fix common OCR mistakes
    text = text.replace("ByTech", "B.Tech")
    text = text.replace('12"', "12th")
    text = text.replace('10"', "10th")
    text = text.replace("Github", "GitHub")

    return clean_text_general(text)


def clean_docx_text(text: str) -> str:
    return clean_text_general(text)