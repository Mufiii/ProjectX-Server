import json
import math
from .models import *
from rest_framework import status
from rest_framework.views import APIView
from .serializer import (
    DeveloperSerializer,
    VendorSerializer,
    UserLoginSerializer,
) 
from django.contrib.sites.shortcuts import get_current_site  
from rest_framework.response import Response
import random
from django.conf import settings
from threading import Thread
from .utils.smtp import send_mail
from .utils.token import get_token_for_user
import base64
import jwt
import hmac
import hashlib
from django.urls import reverse
from .utils import vecode
from rest_framework.generics import GenericAPIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes


class DeveloperRegistrationAPIView(APIView):
    def post(self,request):
        serializer = DeveloperSerializer(data=request.data)
        if serializer.is_valid():
            otp = random.randint(100000,999999)
            request.session['otp'] = otp
            user = User.objects.create(
                email = serializer.validated_data.get('email'),
                is_developer = True,
                is_active = False
            )
            
            email = serializer.validated_data.get('email')
            subject = "otp for Account Verification"
            message = f"Your Otp verifiaction code is {otp}"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
 
            send_mail(subject,message,email_from,recipient_list)

            user.save()
            return Response(
              {'email':email,'Otp':otp},
              status=status.HTTP_201_CREATED
            )
        return Response(
            {serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


class VerifyOtp(APIView):
    def post(self,request):
        email = request.data.get('email')
        entered_otp = request.data.get('entered_otp')
        try :
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'msg':"user not found"})
        otp = request.session.get('otp')
        if str(otp) == str(entered_otp):
            user.is_active = True
            user.save()
            token = get_token_for_user(user)
            return Response(
                {'msg':'Registration Done succesfully','token':token},
                status=status.HTTP_200_OK
            )
        return Response(
            {'msg':"there is an error"},
            status=status.HTTP_400_BAD_REQUEST
        )
        

class VendorRegistrationView(APIView):
    def post(self,request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create(
                email = serializer.validated_data.get('email'),
                first_name = serializer.validated_data.get('first_name'),
                last_name = serializer.validated_data.get('last_name'),
                country = serializer.validated_data.get('country'),
                is_vendor = True,
                is_active = False
            )
            user.save()
            
            encode_header = base64.urlsafe_b64encode(json.dumps({"alg": "HS256" , "typ":"JWT"}).encode()).decode()
            encode_payload = base64.urlsafe_b64encode(json.dumps({"id":user.id,"email":user.email}).encode()).decode()
            
            message = f"{encode_header}.{encode_payload}"
            
            signature = base64.urlsafe_b64encode(hmac.new(settings.SECRET_KEY.encode(), message.encode(), hashlib.sha256).digest()).decode()
            
            token = f"{encode_header}.{encode_payload}.{signature}"
            
            current_site = get_current_site(request).domain
            relativeLink = reverse('email_verify')
            absurl = 'http://'+current_site+relativeLink+"?token=" + str(token)
            email_body = 'Hi '+user.first_name+ ' Use the Link below to Verify Your email \n'+absurl
            data = {'email_body':email_body}
            
            vecode.send_email(data)
            
            return Response(
                {'data':data},
                status=status.HTTP_201_CREATED
            )
            
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class VerifyEmail(generics.GenericAPIView):
    def get(self,request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token,settings.SECRET_KEY,algorithms=["HS256"])
            user = User.objects.get(id=payload['id'])
            if not user.is_active:
                user.is_active = True
                user.save()
                token = get_token_for_user(user)
                return Response(
                    {'token':token},
                    status=status.HTTP_200_OK
                )
        except jwt.ExpiredSignatureError as e:
            return Response(
                {"error":"Activation Expired"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        except jwt.exceptions.DecodeError as e:
            return Response(
              {"error":"Invalid token"},
              status=status.HTTP_400_BAD_REQUEST
            )


class UserLoginRequestAPIView(APIView):
    def post(self,request):
        email = request.data.get('email')

        try:
            otp = math.floor(random.randint(100000,999999))
            request.session['otp'] = otp
            subject = "Otp Verification"
            message = f"Your verification otp is {otp}"
            email_from = settings.EMAIL_HOST_USER
            recipient_email = [email]
            send_mail(subject,message,email_from,recipient_email)
            response_data = {"email": email, "otp": otp}
            return Response(response_data,status=status.HTTP_200_OK)
        except:
            return Response(
                {"msg": "Something Went Wrong..."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

            
class LoginOtpverification(APIView):
    def post(self,request):
        email = request.data.get('email')
        entered_otp = request.data.get('entered_otp')
        try :
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'msg':"user not found"})
        
        otp = request.session.get('otp')
        if str(otp) == str(entered_otp):
            token = get_token_for_user(user)
            return Response({"msg":"User loggined successfully","token":token},
                            status=status.HTTP_200_OK
            )
        return Response(
            {"msg":"invalid otp"},
            status=status.HTTP_400_BAD_REQUEST
        )
        
