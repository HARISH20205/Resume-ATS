import fitz
import json
import re

def clean_text(text):
    text = text.replace("", "").replace("ï", "").replace("§", "").replace("•", "-")
    text = re.sub(r'[^\x00-\x7F]+', '', text)  
    text = re.sub(r'\s+', ' ', text).strip()   
    return text

def extract_pdf_to_json(pdf_path):
    data = {"sections": []}
    with fitz.open(pdf_path) as pdf:
        for page in pdf:
            text = page.get_text("text")
            cleaned_text = clean_text(text)
            data["sections"].append({"page_content": cleaned_text})
    return data

def save_to_json(data, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

pdf_path = "Data/resumen.pdf"
output_file = "outputjson.json"

extracted_data = extract_pdf_to_json(pdf_path)
save_to_json(extracted_data, output_file)

print(f"Data extracted and saved to {output_file}")