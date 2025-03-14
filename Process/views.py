import logging
import traceback
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


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

model_name = "sentence-transformers/all-MiniLM-L6-v2"
logger.info(f"Loading model: {model_name}")
try:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    logger.debug(traceback.format_exc())

def get_embeddings(texts):
    try:
        logger.debug(f"Generating embeddings for {len(texts)} texts")
        inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
        with torch.no_grad():
            model_output = model(**inputs)
        embeddings = model_output.last_hidden_state.mean(dim=1)
        return embeddings
    except Exception as e:
        logger.error(f"Error generating embeddings: {e}")
        logger.debug(traceback.format_exc())
        return None

def calculate_similarity(job_description, resume_text):
    try:
        logger.info("Calculating similarity between job description and resume")
        jd_embedding = get_embeddings([job_description])
        resume_embedding = get_embeddings([resume_text])

        jd_embedding = jd_embedding / jd_embedding.norm(dim=1, keepdim=True)
        resume_embedding = resume_embedding / resume_embedding.norm(dim=1, keepdim=True)
        similarity = torch.mm(jd_embedding, resume_embedding.T).item()
        return similarity
    except Exception as e:
        logger.error(f"Error calculating similarity: {e}")
        logger.debug(traceback.format_exc())
        return 0.0

@csrf_exempt
def process_resume(request):
    if request.method == 'POST':
        try:
            logger.info("Processing resume request")
            data = json.loads(request.body)

            user_id = data.get('user_id')
            file_link = data.get('file_link')
            job_description = data.get('job_description')
            logger.info(f"Received data for user_id: {user_id}")
            
            if not all([user_id, file_link, job_description]):
                logger.warning("Missing required fields in request")
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            logger.info("Extracting Text from the pdf")
            resume = extract_text_from_pdf(file_link)
            logger.info(f"Text extracted from the pdf : {resume}")

            logger.info("Extracting resume details")
            st_data = extract_resume_details(resume)
            logger.info("Resume details extraction completed")

            logger.info("Generating ATS score")
            ats_score = generate_ats_score(st_data, job_description)
            logger.info("ATS score generation completed")

            response_data = {
                'user_id': user_id,
                'similarity': "100.00",
                'ats_score': ats_score,
                'structured_data': st_data
            }
            logger.info("Sending successful response")
            return JsonResponse(response_data, status=200)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON received: {e}")
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            error_msg = f"Error processing resume: {e}"
            logger.error(error_msg)
            logger.debug(traceback.format_exc())
            return JsonResponse({'error': error_msg}, status=500)
    else:
        logger.warning(f"Unsupported method: {request.method}")
        return JsonResponse({'message': 'Only POST requests are allowed'}, status=405)

def verify_api(request):
    logger.info(f"API verification request received via {request.method}")
    if request.method == 'GET':
        return JsonResponse({'message': 'yaay working-GET '}, status=200)
    else:
        logger.warning(f"Unsupported method for API verification: {request.method}")
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)

def home(request):
    logger.info(f"Home request received via {request.method}")
    if request.method == 'GET':
        return JsonResponse({'message': 'Welcome To Resume-ATS'}, status=200)
    else:
        logger.warning(f"Unsupported method for home: {request.method}")
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)