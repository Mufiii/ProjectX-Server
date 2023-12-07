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
from .utils.vecode import send_email
from rest_framework.generics import GenericAPIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics


class DeveloperRegistrationAPIView(APIView):
    @swagger_auto_schema(
        tags=["Authentication"],
        operation_description="Developer Registeration",
        operation_summary="This endpoint is used for Developer registeration",
        request_body=DeveloperSerializer,
        responses={
            201: DeveloperSerializer,
            400: "Bad Request",
            500: "errors",
        },
    )
    
    def post(self,request):
        serializer = DeveloperSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            print("hiiiii")
            otp = random.randint(100000,999999)
            try :
                user = User.objects.create(
                    email = serializer.validated_data.get('email'),
                    first_name = serializer.validated_data.get('first_name'),
                    last_name = serializer.validated_data.get('last_name'),
                    country = serializer.validated_data.get('country'),
                    is_developer = True,
                    is_active = False,
                    otp = otp
                )
                print("Hiiiiiiiii")
                print("user")
                email = serializer.validated_data.get('email')
                subject = "otp for Account Verification"
                message = f"Your Otp verifiaction code is {otp}"
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email]
    
                send_mail(subject,message,email_from,recipient_list)
                user.save()
            except :
                return Response({"msg":"User Already exists"},status=status.HTTP_400_BAD_REQUEST)
            return Response(
              {'email':email,'otp':otp},
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
        if int(user.otp) == int(entered_otp):
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
    @swagger_auto_schema(
        tags=["Authentication"],
        operation_description="Vendor Registeration",
        operation_summary="This endpoint is used for Vendor registeration",
        request_body= VendorSerializer,
        responses={
            200: VendorSerializer,
            400: "bad request",
            500: "errors",
        },
    )
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
                absurl = 'http://'+'localhost:5173'+relativeLink+str(token)
                email_body = 'Hi '+user.first_name+ ' Use the Link below to Verify Your email \n'+absurl
                data = {'email_body':email_body,'to_email':user.email,"email_subject":"verification"}
                
                send_email(data)
                return Response(
                    {'data':data,"token":token},
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
            print(token)
            payload = jwt.decode(token,settings.SECRET_KEY,algorithms=["HS256"])
            print(payload,"kkkkkkkk")
            user = User.objects.get(id=payload['id'])
            if not user.is_active:
                user.is_active = True
                user.save()
                token = get_token_for_user(user)
                return Response(
                    {'token':token},
                    status=status.HTTP_200_OK
                )
            return Response({"msg":"You Already verified Your Email"},status=status.HTTP_400_BAD_REQUEST)
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
        user = User.objects.get(email=email)

        try:
            otp = math.floor(random.randint(100000,999999))
            user.otp = otp
            user.save()
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
        print(entered_otp,'op')
        try :
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'msg':"user not found"})

        if  int(user.otp) == int(entered_otp):
            token = get_token_for_user(user)
            return Response({"msg":"User loggined successfully","token":token},
                            status=status.HTTP_200_OK
            )
        return Response(
            {"msg":"invalid otp"},
            status=status.HTTP_400_BAD_REQUEST
        )
        
