from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
import concurrent.futures

from .response import get_response

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
@csrf_exempt
def process_change(request):
    if request.method == "POST":
        try:
            # Parse JSON only once
            data = json.loads(request.body)

            user_id = data.get('user_id')
            prompt = data.get("prompt")
            content = data.get('content')
            section = data.get("section")
            job_description = data.get('job_description')
            
            if not all([user_id, prompt, content]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            
            # Customize processing approach based on section
            section_specific_instruction = ""
            if section == "skills" or section == "experience" or section == "projects":
                section_specific_instruction = "Format achievements using the X-Y-Z method (e.g., 'Accomplished X as measured by Y, by doing Z'). Provide at least one compelling example that demonstrates measurable impact."
            else:
                section_specific_instruction = "Incorporate relevant keywords from the job description while avoiding generic buzzwords. Focus on specificity and concrete details that align with ATS screening requirements."
            
            combined_prompt = f"Content: {content}\nJob Description: {job_description}\nTask: {prompt}"
            
            system_instruction = """As an ATS resume optimizer, modify the content to match the job requirements while preserving truthfulness. Use the X-Y-Z method to quantify achievements where possible (e.g., "Accomplished X as measured by Y, by doing Z"). Format your response as a clean text without any prefixes or explanations. Do not include any JSON formatting in your actual content modification."""
            
            # Combine system_instruction with section_specific_instruction
            combined_system_instruction = f"{system_instruction} {section_specific_instruction}"
            
            modified_content = get_response(combined_prompt, combined_system_instruction)
            
            return JsonResponse({
                'user_id': user_id,
                'modified_content': modified_content
            }, status=200)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            logger.error(f"Error in process_change: {str(e)}")
            return JsonResponse({'error': 'Processing error'}, status=500)
    else:
        return JsonResponse({'message': 'Only POST requests are allowed'}, status=405)
