import pdfplumber
from pdfplumber.table import T_table_settings


def pdf_to_markdown(pdf_path) -> str:
    md_text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Extract text
            # text = page.extract_text()
            # if text:
            #     md_text += text + "\n\n"

            table_settings: T_table_settings = {
                "vertical_strategy": "lines",
                "horizontal_strategy": "text",
                "intersection_y_tolerance": 10,
                "intersection_x_tolerance": 10,
                "snap_tolerance": 5,
                "join_tolerance": 15,
            }
            tables = page.extract_tables(table_settings)
            filtered_tables: list[list[list[str]]] = []
            for table in tables:
                filtered_table = []
                for row in table:
                    filtered_row = []
                    for cell in row:
                        if cell and cell != "":
                            cell = cell.replace("\n", " ")
                            filtered_row.append(cell)
                    filtered_table.append(filtered_row)
                filtered_tables.append(filtered_table)
            for table in filtered_tables:
                if table:
                    # Add headers
                    headers = table[0]
                    md_text += "| " + " | ".join(str(header) for header in headers) + " |\n"
                    md_text += "| " + " | ".join("---" for _ in headers) + " |\n"
                    
                    # Add table rows
                    for row in table[1:]:
                        md_text += "| " + " | ".join(str(cell) for cell in row) + " |\n"
                md_text += "\n"
    return md_text
