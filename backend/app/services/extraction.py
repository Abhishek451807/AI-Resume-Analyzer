import fitz  # PyMuPDF
import docx
import io

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extracts text from PDF bytes using PyMuPDF."""
    text = ""
    with fitz.open("pdf", file_bytes) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extracts text from DOCX bytes."""
    doc = docx.Document(io.BytesIO(file_bytes))
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text(file_bytes: bytes, filename: str) -> str:
    """Route to correct extractor based on extension."""
    if filename.lower().endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    elif filename.lower().endswith(".docx"):
        return extract_text_from_docx(file_bytes)
    elif filename.lower().endswith(".txt"):
        return file_bytes.decode('utf-8')
    else:
        raise ValueError("Unsupported file format. Please upload PDF, DOCX, or TXT.")
