from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Chat
import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Default prompt template
DEFAULT_PROMPT = "If i give a text you can transform english to french: {text}"

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def index(request):
    return render(request, 'core/index.html', {
        'default_prompt': DEFAULT_PROMPT
    })

def success(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_input = data.get('user_input')
            prompt_template = data.get('prompt_template', DEFAULT_PROMPT)
            system_message = data.get('system_message', '')
            temperature = float(data.get('temperature', 0.0))
            
            if not user_input:
                return JsonResponse({'error': 'No input provided'}, status=400)
            
            # Configure the model
            model = genai.GenerativeModel('gemini-1.5-pro')
            
            # Create the full prompt
            full_prompt = f"{system_message}\n\n{prompt_template.format(text=user_input)}" if system_message else prompt_template.format(text=user_input)
            
            # Generate content
            response = model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    top_p=0.8,
                    top_k=40,
                    max_output_tokens=2048,
                )
            )
            
            # Get the response text
            response_text = response.text

            # Save to database
            chat = Chat.objects.create(
                user_input=user_input, 
                response=response_text,
                prompt_used=prompt_template,
                system_message=system_message
            )
            
            return JsonResponse({
                'user_input': user_input,
                'response': response_text,
                'prompt_template': prompt_template,
                'system_message': system_message
            })
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    return render(request, 'core/index.html')