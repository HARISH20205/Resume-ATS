import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from transformers import AutoTokenizer, AutoModel
import torch
import os

from .ats_parser import extract_resume_details
from .utils import generate_ats_score
from .response import get_response
from .extract import extract_text_from_pdf

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the model and tokenizer globally to avoid reloading them for every request
model_name = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

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
            logger.info(f"Received data for user: {user_name}, user_id: {user_id}")

            similarity = calculate_similarity(job_description, resume)
            logger.info("Similarity calculation completed")

            st_data = extract_resume_details(resume)
            logger.info("Resume details extraction completed")

            ats_score = generate_ats_score(st_data, job_description)
            logger.info("ATS score generation completed")

            response_data = {
                'user_id': user_id,
                'user_name': user_name,
                'similarity': similarity,
                'ats_score': ats_score,
                'structured_data': st_data
            }
            return JsonResponse(response_data, status=200)
        except json.JSONDecodeError:
            logger.error("Invalid JSON received")
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    elif request.method == 'GET':
        return JsonResponse({'message': 'yaay working '}, status=200)
    else:
        return JsonResponse({'error': 'Only POST and GET requests are allowed'}, status=405)

def verify_api(request):
    if request.method == 'GET':
        return JsonResponse({'message': 'yaay working-GET '}, status=200)
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)