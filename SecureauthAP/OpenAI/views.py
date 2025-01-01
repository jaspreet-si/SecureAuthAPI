from django.shortcuts import render
from .utils import OpenAI
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import request , status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated



class OpenAIChat(APIView):
  
  permission_classes = [IsAuthenticated]

  def post(self,request):
      prompt = request.data.get('prompt')
      if prompt:  
          try:
              response = OpenAI.generate_response(prompt)
              print("response in the openaichat",response)
              return Response({"Response":response},status=status.HTTP_201_CREATED)
          except Exception as e:
              return Response({"Erro":str(e)},status=status.HTTP_400_BAD_REQUEST)
      else:
          return Response({"Error":"Prompt not provided"},status=status.HTTP_204_NO_CONTENT)
      
          