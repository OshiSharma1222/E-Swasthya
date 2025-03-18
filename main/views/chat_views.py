from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from ..ai_handler import ai_handler
from ..symptom_checker import symptom_checker
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["POST"])
def process_chat(request):
    try:
        # Parse request body
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON format'
            }, status=400)

        # Validate input
        if not user_message:
            return JsonResponse({
                'status': 'error',
                'message': 'Message cannot be empty'
            }, status=400)

        # First, check for symptoms using Gemini model
        try:
            symptom_result = symptom_checker.check_symptoms(user_message)
            if symptom_result['status'] == 'error':
                logger.error(f"Symptom checker error: {symptom_result['message']}")
        except Exception as e:
            logger.error(f"Symptom checker exception: {str(e)}")
            symptom_result = {'status': 'error', 'message': str(e)}
        
        # Get response from Gemini AI
        try:
            ai_response = ai_handler.get_response(
                user_message, 
                symptom_result if symptom_result['status'] == 'success' else None
            )
            
            if ai_response['status'] == 'error':
                logger.error(f"AI handler error: {ai_response['response']}")
                return JsonResponse({
                    'status': 'error',
                    'message': 'Failed to generate response',
                    'details': ai_response['response']
                }, status=500)
                
        except Exception as e:
            logger.error(f"AI handler exception: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': 'Failed to process message',
                'details': str(e)
            }, status=500)

        return JsonResponse({
            'status': 'success',
            'response': ai_response['response'],
            'symptom_analysis': symptom_result if symptom_result['status'] == 'success' else None
        })

    except Exception as e:
        logger.error(f"General process_chat exception: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': 'Internal server error',
            'details': str(e)
        }, status=500) 