from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Chat
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os
import json

load_dotenv()

# Default prompt template
DEFAULT_PROMPT = "If i give a text you can transform english to french: {text}"

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
            
            llm = ChatOpenAI(
                model="gpt-4o", 
                temperature=temperature,
                api_key=os.getenv("OPENAI_API_KEY")
            )

            # Create the full prompt with system message if provided
            if system_message:
                prompt = ChatPromptTemplate.from_messages([
                    ("system", system_message),
                    ("user", prompt_template)
                ])
            else:
                prompt = ChatPromptTemplate.from_template(prompt_template)

            chain = prompt | llm | StrOutputParser()
            response = chain.invoke({"text": user_input})

            # Save to database
            chat = Chat.objects.create(
                user_input=user_input, 
                response=response,
                prompt_used=prompt_template,
                system_message=system_message
            )
            
            return JsonResponse({
                'user_input': user_input,
                'response': response,
                'prompt_template': prompt_template,
                'system_message': system_message
            })
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    return render(request, 'core/index.html')