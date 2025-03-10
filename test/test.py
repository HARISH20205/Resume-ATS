from google import genai
from google.genai import types

import requests

image_path = "https://firebasestorage.googleapis.com/v0/b/verbisense.appspot.com/o/uploads%2FicFk6CDLPCPwaV8mOyShdLeyB7f2%2FResume-1.pdf?alt=media&token=3a0f8b9d-ece3-4bda-b25c-a55cc16bede2"
image = requests.get(image_path)

client = genai.Client(api_key="AIzaSyClYvVaQYvV9SjxRttOiPo2sTda2drVOg8")
response = client.models.generate_content(
    model="gemini-2.0-flash-exp",
    contents=["extract the text and give in json format",
              types.Part.from_bytes(data=image.content, mime_type="image/jpeg")])

print(response.text)




# import fitz
# import json
# import re

# def clean_text(text):
#     text = text.replace("", "").replace("ï", "").replace("§", "").replace("•", "-")
#     text = re.sub(r'[^\x00-\x7F]+', '', text)  
#     text = re.sub(r'\s+', ' ', text).strip()   
#     return text

# def extract_pdf_to_json(pdf_path):
#     data = {"sections": []}
#     with fitz.open(pdf_path) as pdf:
#         for page in pdf:
#             text = page.get_text("text")
#             cleaned_text = clean_text(text)
#             data["sections"].append({"page_content": cleaned_text})
#     return data

# def save_to_json(data, output_file):
#     with open(output_file, "w", encoding="utf-8") as file:
#         json.dump(data, file, indent=4, ensure_ascii=False)

# pdf_path = "Data/resumen.pdf"
# output_file = "outputjson.json"

# extracted_data = extract_pdf_to_json(pdf_path)
# save_to_json(extracted_data, output_file)

# print(f"Data extracted and saved to {output_file}")