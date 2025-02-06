from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from transformers import AutoTokenizer, AutoModel
import torch
import fitz

from ats_score.utils import generate_ats_score

# Load the model and tokenizer globally to avoid reloading them for every request
model_name = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

def extract_text_from_pdf(file_path):
    text = ""
    doc = fitz.open(file_path)
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

def get_embeddings(texts):
    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        model_output = model(**inputs)
    embeddings = model_output.last_hidden_state.mean(dim=1)
    return embeddings

def calculate_similarity(job_description, resume_text):
    jd_embedding = get_embeddings([job_description])
    resume_embedding = get_embeddings([resume_text])

    jd_embedding = jd_embedding / jd_embedding.norm(dim=1, keepdim=True)
    resume_embedding = resume_embedding / resume_embedding.norm(dim=1, keepdim=True)
    similarity = torch.mm(jd_embedding, resume_embedding.T).item()
    return similarity

@csrf_exempt
def process_resume(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            user_name = data.get('user_name')
            user_id = data.get('user_id')
            resume = data.get('resume')
            job_description = data.get('job_description')

            similarity = calculate_similarity(job_description, resume)
            ats_score = generate_ats_score(resume,job_description)
            response_data = {
                'user_id': user_id,
                'user_name': user_name,
                'similarity': similarity,
                'ats_score':ats_score
            }

            return JsonResponse(response_data, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    elif request.method == 'GET':
        return JsonResponse({'message': 'yaay working '}, status=200)
    else:
        return JsonResponse({'error': 'Only POST and GET requests are allowed'}, status=405)

def verify_api(request):
    if request.method == 'GET':
        return JsonResponse({'message': 'yaay working '}, status=200)
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)