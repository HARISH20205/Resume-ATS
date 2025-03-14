import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import requests

def extract_text_from_pdf(file_path_or_url):
    text = ""
    
    # Check if the file_path_or_url is a URL
    if file_path_or_url.startswith(('http://', 'https://')):
        # Download the PDF file from URL
        response = requests.get(file_path_or_url)
        if response.status_code != 200:
            raise Exception(f"Failed to download the file: {response.status_code}")
        
        # Open the PDF from the downloaded bytes
        doc = fitz.open(stream=io.BytesIO(response.content), filetype="pdf")
    else:
        # Open the PDF from a local file path
        doc = fitz.open(file_path_or_url)

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

# Example usage with Firebase URL
# firebase_url = "https://firebasestorage.googleapis.com/v0/b/resumeats-50ccf.firebasestorage.app/o/uploads%2Fsanthoshrajan776%40gmail.com%2FSanthoshNatarajan_InternshalaResume%20(1).pdf?alt=media&token=f11f9601-6550-4e64-bba6-a2b699a148af"
# text = extract_text_from_pdf(firebase_url)
# print(text)
