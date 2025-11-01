from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import requests
import json

def index(request):
    return render(request, 'chat/index.html')

@csrf_exempt
def chat_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            
            if not user_message:
                return JsonResponse({'error': 'No message provided'}, status=400)
            
            # Groq API Configuration
            API_KEY = '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'
            API_URL = 'https://api.groq.com/openai/v1/chat/completions'
            
            # Make request to Groq
            response = requests.post(
                API_URL,
                headers={
                    'Authorization': f'Bearer {API_KEY}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'llama-3.1-8b-instant',
                    'messages': [
                        {'role': 'user', 'content': user_message}
                    ],
                    'temperature': 0.7,
                    'max_tokens': 1000
                }
            )
            
            if response.status_code == 200:
                ai_response = response.json()['choices'][0]['message']['content']
                return JsonResponse({
                    'response': ai_response,
                    'success': True
                })
            else:
                return JsonResponse({
                    'error': f'API Error: {response.status_code}',
                    'success': False
                }, status=500)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            
            return JsonResponse({
                'error': str(e),
                'success': False
            }, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)