from accounts.auth import Authentication
from accounts.models import User
from accounts.serializers import UserSerializer
from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


class Signin(APIView):
    def post(self, request):
        login = request.data.get('login')
        password = request.data.get('password')

        auth = Authentication()
        try:
            user = auth.signin(login=login, password=password)
        except Exception as e:
            return Response(
                {'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED
                )

        token = RefreshToken.for_user(user)

        serializer = UserSerializer(user)

        return Response({
            "user": serializer.data,
            "refresh": str(token),
            "access": str(token.access_token)
        })


class Signup(APIView):
    def post(self, request):
        name = request.data.get('name')
        lastname = request.data.get('lastname')
        login = request.data.get('login')
        email = request.data.get('email')
        password = request.data.get('password')
        cargo = request.data.get('cargo')
        is_manager = request.data.get('is_manager', False)

        auth = Authentication()

        try:
            with transaction.atomic():
                user = auth.signup(
                    name=name,
                    lastname=lastname,
                    login=login,
                    email=email,
                    password=password,
                    cargo=cargo,
                    is_manager=is_manager
                )
        except Exception as e:
            return Response(
                {'error': str(e)}, status=status.HTTP_400_BAD_REQUEST
                )

        serializer = UserSerializer(user)
        return Response(
            {"user": serializer.data}, status=status.HTTP_201_CREATED
            )


class GetUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response({"user": serializer.data}, status=status.HTTP_200_OK)
