import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

def extract_text_from_pdf(file_path):
    text = ""
    doc = fitz.open(file_path)

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        # Try to extract text
        page_text = page.get_text()
        
        if page_text.strip():  # If text is found
            text += page_text
        else:  # If no text, use OCR
            pix = page.get_pixmap()
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            ocr_text = pytesseract.image_to_string(img)
            text += ocr_text

    return text

# file_path = "../Data/resumen.pdf"
# text = extract_text_from_pdf(file_path)
# print(text)
