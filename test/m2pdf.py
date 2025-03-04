# import fitz  # PyMuPDF

# def pdf_to_markdown(pdf_file_path, markdown_file_path):
#     # Open the PDF file
#     pdf_document = fitz.open(pdf_file_path)

#     # Extract text from each page and format it as markdown
#     markdown_content = ""
#     for page_number in range(len(pdf_document)):
#         page = pdf_document[page_number]
#         text = page.get_text("text")
        
#         # Append a header for the page (optional)
#         markdown_content += f"# Page {page_number + 1}\n\n"
#         markdown_content += text + "\n\n"
    
#     # Save the markdown content to a file
#     with open(markdown_file_path, "w", encoding="utf-8") as markdown_file:
#         markdown_file.write(markdown_content)
    
#     print(f"Markdown file generated at: {markdown_file_path}")

# # Example usage
# pdf_to_markdown("Data/Resume.pdf", "Harish_KB_Resume.md")






from markdown2 import markdown
from weasyprint import HTML

with open("readme1.md") as f:
    raw_markdown = f.read()

processed_markdown = raw_markdown.replace(r"\n", "\n")

html_content = markdown(processed_markdown)

pdf_file_path = "Harish_KB_Resume.pdf"
HTML(string=html_content).write_pdf(pdf_file_path)

print(f"PDF generated at {pdf_file_path}")
