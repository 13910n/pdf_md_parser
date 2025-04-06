import fitz  # PyMuPDF


def pdf_to_markdown(pdf_path) -> str:
    doc = fitz.open(pdf_path)
    md_text = ""

    for page in doc:
        blocks = page.get_text("blocks")
        for block in blocks:
            x, y, w, h, text, block_no, block_type = block
            if block_type == 0:  # Text block
                md_text += text.strip() + "\n\n"

    # Simple formatting (adjust as needed)
    md_text = md_text.replace("**", "**")  # Bold detection (basic)

    return md_text
