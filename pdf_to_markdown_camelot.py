import camelot.io as camelot
from tabulate import tabulate

def pdf_to_markdown(pdf_path) -> str:
    # Extract tables using Camelot (flavor="lattice" for bordered tables)
    tables = camelot.read_pdf(pdf_path, pages="all")
    
    markdown_content = ""
    for i, table in enumerate(tables):
        # Convert Camelot table to Pandas DataFrame
        df = table.df
        
        # Convert DataFrame to Markdown using tabulate
        markdown_table = tabulate(df, headers="keys", tablefmt="pipe")
        
        # Append to Markdown content
        markdown_content += f"### Table {i + 1}\n\n"
        markdown_content += markdown_table + "\n\n"
    
    print(f"Extracted {len(tables)} tables")
    return markdown_content
