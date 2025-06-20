import fitz  # PyMuPDF
import docx2txt
import re
import os

def extract_text_from_pdf(path):
    doc = fitz.open(path)
    return "\n".join([page.get_text() for page in doc])

def extract_text_from_docx(path):
    return docx2txt.process(path)

def extract_email(text):
    match = re.search(r"[\w.-]+@[\w.-]+\.\w+", text)
    return match.group() if match else ""

def extract_phone(text):
    match = re.search(r"(?:\+91\s*|0)?[6-9]\d{9}", text)
    return match.group() if match else ""

def extract_skills(text, keywords):
    return list(set([skill for skill in keywords if skill.lower() in text.lower()]))

def extract_experience(text):
    match = re.search(r"(\d+)\s+years", text.lower())
    return int(match.group(1)) if match else 0

def extract_name(text):
    lines = text.split("\n")
    return lines[0] if lines else "Unknown"

def parse_resume(path, skill_keywords):
    ext = os.path.splitext(path)[1].lower()
    text = extract_text_from_pdf(path) if ext == ".pdf" else extract_text_from_docx(path)
    return {
        "Name": extract_name(text),
        "Email": extract_email(text),
        "Phone": extract_phone(text),
        "Skills": extract_skills(text, skill_keywords),
        "Experience": extract_experience(text),
        "Location": "",
        "Resume File": os.path.basename(path)
    }
