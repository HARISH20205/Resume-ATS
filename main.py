import fitz 
def get_text(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num) 
        text += page.get_text() 
    return text


pdf_path = "Data/Resume.pdf"
extracted_text = get_text(pdf_path)
print(extracted_text)