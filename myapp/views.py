import json
from django.http import JsonResponse
from mysqlx import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from .models import User
from .serializers import UserSerializer

class LoginView(APIView):
    def post(self, request, format=None):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)

        if user.check_password(password):
            # Here, you would generate a JWT or similar token and return it in the response.
            # For this example, we'll just return the user data.
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)

class SignupView(APIView):
    def post(self, request):
        data = request.data

        email = data.get('email')
        password = data.get('password')
        name = data.get('name', '')

        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'error': 'User with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User(
            email=email,
            name=name
        )
        user.set_password(password)
        user.save()

        return Response({'message': 'Signup successful', 'user': {'email': user.email, 'name': user.name}}, status=status.HTTP_201_CREATED)