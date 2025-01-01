import openai
from django.conf import settings
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from openai import OpenAI

client = OpenAI(api_key = settings.OPENAI_API_KEY)

# openai.api_key = settings.OPENAI_API_KEY

class OpenAI:
    @staticmethod
    def generate_response(prompt):
       
        try:
            print("try part ")
            response =  client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": prompt}
                    ]  
            )
            ai_message = response.choices[0].message.content
            return ai_message
        except Exception as e:
            return {"Error": str(e)}
        
        
    