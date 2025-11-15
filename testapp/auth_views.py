#django imports
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from testapp.utils import api_success, api_error

#rest-framework import
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class RegisterAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")
        confirm_password = request.data.get("confirm_password")

        if not username or not password or not confirm_password or not email:
            return api_error("All fields are required")

        if User.objects.filter(username = username).exists():
            return api_error("Username already exists.")
        
        if User.objects.filter(email = email).exists():
            return api_error("Email already existrs.")
        if password != confirm_password:
            return api_error("Password do not match")
        
        user = User.objects.create_user(
            username=username , 
            password=password,
            email= email
        )
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)
        
        return api_success(
            payload={"access": access, "refresh": str(refresh)},
            message="Registration successful"
        )


class LoginAPIView(APIView):
    def post(self,request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username = username , password = password)

        if user is None:
            return api_error(
                "Invalid credentials",
                http_status=status.HTTP_401_UNAUTHORIZED
            )
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)
        
        return api_success(
            payload={"access": access, "refresh": refresh},
            message="Login successful"
        )
