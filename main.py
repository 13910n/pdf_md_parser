import os
from helper import print_memory_usage
from pdf_to_markdown_hybrid import pdf_to_markdown

if __name__ == "__main__":
    example_dir = "example"
    output_dir = "output_hybrid"

    os.makedirs(output_dir, exist_ok=True)
    results: list[tuple[str, int]] = []

    for filename in os.listdir(example_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(example_dir, filename)
            output_md = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.md")
            print(f"Processing {filename}...")
            before_memory = print_memory_usage()
            text = pdf_to_markdown(pdf_path)
            after_memory = print_memory_usage()
            results.append((filename, after_memory - before_memory))
            with open(output_md, 'w', encoding='utf-8') as f:
                f.write(text)
    print("Done")
    print(results)
    max_memory_used: tuple[str, int] = max(results, key=lambda x: x[1])
    print("Max memory used: ", max_memory_used[1], "MB for file: ", max_memory_used[0])
