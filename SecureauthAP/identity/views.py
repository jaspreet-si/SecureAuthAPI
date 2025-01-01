from django.shortcuts import render
from .models import User , FcmDeviceId , OTP
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import  SignUpSerializer
from rest_framework import status
from django.utils import timezone
from datetime import timedelta

# for the authentication token and authorization
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password,check_password

# for the email 
from django.core.mail import EmailMultiAlternatives,send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


from rest_framework.permissions import AllowAny
import math
import random
import secrets

def generateOTP():
    return ''.join([str(secrets.choice(range(6))) for _ in range(6)])


def send_otp_email(user_email, OTP):
  try:
      subject = "Welcome to [Your Service Name]"
      from_email = 'jas95920@gmail.com'
      to_email = [user_email]

      # Render email template
      html_content = render_to_string('send_email_template.html', {'OTP':OTP})
      text_content = strip_tags(html_content)

      # Create and send email
      email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
      email.attach_alternative(html_content, "text/html")

      try:
        email.send()
      except Exception as e:
        print(e)
      
  except Exception as e:
    return Response(e)

class SignUp(APIView):
  permission_classes = [AllowAny]
  def post(self , request):
    print("signup api")
    userdata = request.data
    serializer = SignUpSerializer(data=userdata)
    if serializer.is_valid():
      otp = generateOTP()
      OTP.objects.create(email = serializer.validated_data['email'] , otp = otp)
      send_otp_email(serializer.validated_data['email'], otp)
      return Response(
        {"Message":"OTP has been sent to your email","OTP": otp } , status=status.HTTP_201_CREATED
      )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  
class VerifySignUp(APIView):
  def post(self,request):
    email = request.data.get('email')
    otp = request.data.get('OTP')

    try :
      otp_record = OTP.objects.get(email=email,otp=otp)
    except OTP.DoesNotExist:
      return Response({"Error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
    
    if otp_record.created_at < timezone.now() - timedelta(seconds=60):
      otp_record.delete()
      return Response({'error': 'OTP has expired'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
      username = request.data.get('username')
      password = make_password(request.data.get('password'))
      
      User.objects.create(email=email,username=username,password=password)
  
      otp_record.delete()
      
      return Response("User created successfully",status=status.HTTP_201_CREATED)
    except Exception as e:
      return Response({"something went wrong" : {e}},status=status.HTTP_400_BAD_REQUEST)
    

class Login(APIView):
  def post(self,request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    try:
      if '@' in username:
        user = User.objects.get(email=username)
      else:
        user = User.objects.get(username=username)
      
      if user.check_password(password):
        token,_ = Token.objects.get_or_create(user_id=user.id)
        return Response(
          {"Token":token.key},status=status.HTTP_201_CREATED
      )
        
    except User.DoesNotExist:
      return Response({'error':'Invalid Credentials'}, status=
                status.HTTP_400_BAD_REQUEST)

      
      
      
    