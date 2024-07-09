from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.views  import Response
from .serializers import RegisterSerializer, EmailVerificationSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util
import jwt
import os
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Create your views here.


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = get_user_model().objects.get(email=serializer.data['email'])
        token = RefreshToken.for_user(user).access_token
        
        current_site = get_current_site(request).domain
        verify_link = reverse('email-verify')
        absurl = 'http://'+current_site+verify_link+"?token="+str(token)
        email_body = f'Click the link to verify your email \n {absurl}'
        data = {
            'email_body':email_body,
            'to_email':[serializer.data['email']],
            'email_subject':'Verify your email'
            }
        
        Util.send_email(data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class VerifyEmail(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, os.environ.get('SECRET_KEY'), algorithms=["HS256"])
            user = get_user_model().objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email':'Email activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error':'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error':'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)