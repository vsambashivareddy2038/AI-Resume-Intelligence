import pymupdf
from docx import Document


def extract_text_from_pdf(file_path):
    """
    Extract text from every page of a PDF.
    """

    text = ""

    document = pymupdf.open(file_path)

    for page in document:
        page_text = page.get_text()

        if page_text:
            text += page_text + "\n"

    document.close()

    return text.strip()


def extract_text_from_docx(file_path):
    """
    Extract text from a DOCX document.
    """

    document = Document(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:

        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    return "\n".join(paragraphs)


def extract_resume_text(file_path):
    """
    Detect the file type and extract text.
    """

    if file_path.lower().endswith(".pdf"):

        return extract_text_from_pdf(file_path)

    elif file_path.lower().endswith(".docx"):

        return extract_text_from_docx(file_path)

    else:

        raise ValueError(
            "Unsupported file format. "
            "Please upload a PDF or DOCX file."
        )