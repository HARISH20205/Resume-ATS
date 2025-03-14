import json
import logging
import traceback
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .response import get_response

# Set up logging
logger = logging.getLogger(__name__)

@csrf_exempt
def process_change(request):
    logger.info("Change request received")
    if request.method == "POST":
        try:
            logger.info("Processing POST request for content change")
            data = json.loads(request.body)
            logger.debug("Request body parsed successfully")

            user_id = data.get('user_id')
            prompt = data.get("prompt")
            content = data.get('content')
            section = data.get("section")
            job_description = data.get('job_description')
            
            logger.debug(f"Request for user_id: {user_id}, section: {section}")
            
            if not all([user_id, prompt, content]):
                logger.warning("Missing required fields in request")
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            
            # Customize processing approach based on section
            logger.info(f"Customizing instructions for section: {section}")
            section_specific_instruction = ""
            if section == "skills" or section == "experience" or section == "projects":
                section_specific_instruction = "Format achievements using the X-Y-Z method (e.g., 'Accomplished X as measured by Y, by doing Z'). Provide at least one compelling example that demonstrates measurable impact."
            else:
                section_specific_instruction = "Incorporate relevant keywords from the job description while avoiding generic buzzwords. Focus on specificity and concrete details that align with ATS screening requirements."
            
            combined_prompt = f"Content: {content}\nJob Description: {job_description}\nTask: {prompt}"
            
            system_instruction = """As an ATS resume optimizer, modify content to match job requirements while maintaining truthfulness. Quantify achievements using X-Y-Z method where possible. Keep response to 20 words maximum. Return only the modified content in this JSON format:
            {
                "modified_content": "Your concise 20-word max content here"
            }
            """
            
            # Combine system_instruction with section_specific_instruction
            combined_system_instruction = f"{system_instruction} {section_specific_instruction}"
            
            logger.info("Sending request to get_response function")
            modified_content = get_response(combined_prompt, combined_system_instruction)
            logger.info("Content modification completed successfully")
            
            return JsonResponse({
                'user_id': user_id,
                'modified_content': modified_content
            }, status=200)
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON format: {e}")
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            error_msg = f"Error in process_change: {e}"
            logger.error(error_msg)
            logger.debug(traceback.format_exc())
            return JsonResponse({'error': error_msg}, status=500)
    else:
        logger.warning(f"Unsupported method: {request.method}")
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
