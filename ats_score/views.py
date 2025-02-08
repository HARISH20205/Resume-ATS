from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .utils import generate_ats_score

# Create your views here.

@csrf_exempt
def score(request):
    if request.method=='POST':
        try:
            data = json.loads(request.body)
            
            user_name = data.get('user_name')
            user_id = data.get('user_id')
            resume = data.get('resume')
            job_description = data.get('job_description')

            score = generate_ats_score(resume,job_description)
            response_data = {
                "score":score,
                'user_name':user_name
            }
            return JsonResponse(response_data,status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)






def check(request):
    if request.method == 'GET':
        return JsonResponse({'message': 'ATS view working'}, status=200)
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)