from django.core.mail import EmailMessage  
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
import users

from users.api.serializers import OTPSerializer, RegistrationSerializer
from users import models
import random


from django.template.loader import render_to_string 
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode
from project.token import account_activation_token 
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from django.utils.decorators import method_decorator

@api_view(['POST',])
def signup(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        print(serializer)

        if serializer.is_valid():
            newuser = serializer.save()
            print(newuser)
            newuser.is_active = False
            newuser.save()
            current_site = get_current_site(request)
            otp = random.randint(1000,9999)
            otpdata = {
                'user':newuser.pk,
                'otp':otp
            }
            otpserializer = OTPSerializer(data=otpdata)
            print(otpdata)
            print(otpserializer)
            if otpserializer.is_valid():
                otpserializer.save()
            mail_subject = "Activation link has been sent to your email"
            message = render_to_string('acc_active_email.html', {  
                'user': newuser,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(newuser.pk)),  
                'token':account_activation_token.make_token(newuser),  
                'otp':otp
            })  
            to_email = newuser.email
            email = EmailMessage(  
                mail_subject, message, to=[to_email]  
            )  
            email.send()
            resdata ={"newuser":newuser.pk}
            return Response(resdata,status=status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST',])
def verifyuser(request):
    if request.method == 'POST':
        serializer = OTPSerializer(data=request.data)
        resdata = {}
        
        if serializer.is_valid():
            print(serializer.data['user'])
            data = models.OTP.objects.filter(user__icontains=serializer.data['user'],otp__icontains=serializer.data['otp'])
            if data.exists():
                user = User.objects.get(pk = serializer.data['user'])
                user.is_active = True
                user.save()
                resdata['response'] = "Registration Successful!"
                resdata['username'] = user.username

                refresh = RefreshToken.for_user(user)
                resdata['token'] = {
                                'refresh': str(refresh),
                                'access': str(refresh.access_token),
                            }
                return Response(resdata, status=status.HTTP_201_CREATED)
            else:
                errorMessage = {
                    "code":"400",
                    "message":"Wrong Pin"
                    }
                return Response(errorMessage, status=status.HTTP_201_CREATED)
       
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST',])
def logout_view(request): 

    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(['POST',])  
def registration_view(request): 

    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        
        data = {}
        
        if serializer.is_valid():
            account = serializer.save()
            
            data['response'] = "Registration Successful!"
            data['username'] = account.username
            data['email'] = account.email

            refresh = RefreshToken.for_user(account)
            data['token'] = {
                                'refresh': str(refresh),
                                'access': str(refresh.access_token),
                            }
            return Response(data, status=status.HTTP_201_CREATED)
       
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)



class GetUser(APIView):
    @method_decorator(login_required) 
    def get(self,request):
        print("Helo")
        profile = {
            "username":request.user.username,
            "email":request.user.email
            }
        print(profile)
        return Response(profile, status=status.HTTP_201_CREATED)

        
        