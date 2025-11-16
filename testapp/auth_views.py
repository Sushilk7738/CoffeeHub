#django imports
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from testapp.utils import api_success, api_error
from testapp.utils_auth import generate_tokens

#rest-framework import
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class RegisterAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        confirm_password = request.data.get("confirm_password")

        if not all([username, email, password, confirm_password]):
            return api_error("All fields are required")

        if User.objects.filter(username=username).exists():
            return api_error("Username already exists")

        if User.objects.filter(email=email).exists():
            return api_error("Email already exists")

        if password != confirm_password:
            return api_error("Passwords do not match")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        tokens = generate_tokens(user)

        return api_success(tokens, "Registration successful")

class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return api_error("Username and password are required")

        user = authenticate(username=username, password=password)
        if user is None:
            return api_error("Invalid credentials", http_status=401)

        tokens = generate_tokens(user)

        return api_success(tokens, "Login successful")