from inspect import currentframe
from django.shortcuts import render
from rest_framework import generics, serializers,status
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from incomeexpensesapi.settings import SECRET_KEY
# Create your views here.

class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self,request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data

        user = User.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relativeLink='/auth/email-verify/'

        

        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        
        email_body = 'Hi '+user.username+' Use Link below to verify your email \n'+''+absurl+''
        data = {'email_body':email_body,'email_subject':'Verify yur Email','email':user.email}

        Util.send_email(data)

        return Response(user_data,status=status.HTTP_201_CREATED)

class VerifyEmail(generics.GenericAPIView):

    def get(self,request):
        token=request.GET.get('token')
        print(f"token : {token}")
        try:
            payload = jwt.decode(token,SECRET_KEY)
            print(f"payload : {payload}")
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response({'email':'Successfully Activated'},status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as e:
            return Response({'error':'Activation Expired'},status=status.HTTP_400_BAD_REQUEST)
        
        except jwt.exceptions.DecodeError as e:
            return Response({'error':'Invalid Token'},status=status.HTTP_400_BAD_REQUEST)