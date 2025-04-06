import os
import time
from typing import Dict, List, Union
import pandas as pd
from helper import print_memory_usage

# Import all available PDF-to-Markdown converters
from pdf_to_markdown_pdfminer import pdf_to_markdown as pdf_to_markdown_pdfminer
from pdf_to_markdown_fitz import pdf_to_markdown as pdf_to_markdown_fitz
from pdf_to_markdown_camelot import pdf_to_markdown as pdf_to_markdown_camelot
from pdf_to_markdown_pdfplumber import pdf_to_markdown as pdf_to_markdown_pdfplumber
from pdf_to_markdown_hybrid import pdf_to_markdown as pdf_to_markdown_hybrid

def run_statistics():
    example_dir = "example"
    
    # Map of converter functions and their output directories
    converters = {
        "pdfminer": (pdf_to_markdown_pdfminer, "output_pdfminer"),
        "fitz": (pdf_to_markdown_fitz, "output_fitz"),
        "camelot": (pdf_to_markdown_camelot, "output_camelot"),
        "pdfplumber": (pdf_to_markdown_pdfplumber, "output_pdfplumber"),
        "hybrid": (pdf_to_markdown_hybrid, "output_hybrid"),
    }
    
    # Statistics storage - collect simple dictionaries
    results = []
    
    # Process each PDF with each converter
    for filename in sorted(os.listdir(example_dir)):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(example_dir, filename)
            file_size = os.path.getsize(pdf_path) / (1024 * 1024)  # MB
            
            print(f"\nProcessing {filename} (Size: {file_size:.2f} MB)...")
            
            for name, (converter, output_dir) in converters.items():
                print(f"  Using {name}...")
                os.makedirs(output_dir, exist_ok=True)
                output_md = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.md")
                
                try:
                    # Measure memory and time
                    before_time = time.time()
                    before_memory = print_memory_usage()
                    
                    # Run conversion
                    text = converter(pdf_path)
                    
                    after_memory = print_memory_usage()
                    after_time = time.time()
                    
                    # Calculate stats
                    memory_used = after_memory - before_memory
                    execution_time = after_time - before_time
                    
                    # Store stats as a simple dictionary
                    results.append({
                        "converter": name,
                        "filename": filename,
                        "file_size_mb": file_size,
                        "memory_mb": memory_used,
                        "time_sec": execution_time,
                        "has_error": False
                    })
                    
                    # Save output
                    with open(output_md, 'w', encoding='utf-8') as f:
                        f.write(text)
                        
                    print(f"    Memory: {memory_used:.2f} MB, Time: {execution_time:.2f} sec")
                except Exception as e:
                    print(f"    Error: {str(e)}")
                    # Store error stats
                    results.append({
                        "converter": name,
                        "filename": filename,
                        "file_size_mb": file_size,
                        "memory_mb": -1,
                        "time_sec": -1,
                        "has_error": True,
                        "error_message": str(e)
                    })
    
    # Generate statistics report
    generate_statistics_report(results)

def generate_statistics_report(results: List[Dict[str, Union[str, float, int, bool]]]):
    # Save to CSV for reference
    df = pd.DataFrame(results)
    df.to_csv("pdf_conversion_stats.csv", index=False)
    
    # Generate markdown report
    generate_markdown_report(results)
    
    # Print simple summary
    print("\n=== SUMMARY ===")
    filenames = set(item["filename"] for item in results)
    print(f"Total files processed: {len(filenames)}")
    print(f"Results saved to conversion_stats.md")

def generate_markdown_report(results: List[Dict[str, Union[str, float, int, bool]]]):
    """Generate a simple markdown report with conversion statistics"""
    
    # Create the markdown content
    md_content = "# PDF Conversion Statistics\n\n"
    
    # Add file processing stats
    md_content += "## File Processing Statistics\n\n"
    
    # Create table headers
    md_content += "| File | Converter | File Size (MB) | Memory Usage (MB) | Execution Time (sec) |\n"
    md_content += "|------|-----------|----------------|-------------------|---------------------|\n"
    
    # Sort by filename first, then by converter
    # Using Python's sorted instead of pandas
    sorted_results = sorted(results, key=lambda x: (x["filename"], x["converter"]))
    
    # Generate rows
    for item in sorted_results:
        if item["has_error"]:
            # If there was an error, indicate it in the table
            md_content += f"| {item['filename']} | {item['converter']} | {item['file_size_mb']:.2f} | ERROR | ERROR |\n"
        else:
            md_content += f"| {item['filename']} | {item['converter']} | {item['file_size_mb']:.2f} | {item['memory_mb']:.2f} | {item['time_sec']:.2f} |\n"
    
    # Save the markdown file
    with open("conversion_stats.md", "w") as f:
        f.write(md_content)

if __name__ == "__main__":
    run_statistics()
