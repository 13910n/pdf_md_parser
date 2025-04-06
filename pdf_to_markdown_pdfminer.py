from pdfminer.high_level import extract_text
import re


def pdf_to_markdown(pdf_path) -> str:
    text = extract_text(pdf_path)
    # Basic formatting (customize as needed)
    text = re.sub(r'\n{3,}', '\n\n', text)  # Remove excessive newlines
    text = re.sub(r'^\s*•\s*', '- ', text, flags=re.MULTILINE)  # Bullet points
    text = re.sub(r'(?<=\n)([A-Z][^\n]+)\n',
                  r'## \1\n', text)  # Simple headings
    return text
