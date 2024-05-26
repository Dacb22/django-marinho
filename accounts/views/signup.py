from accounts.auth import Authentication
from accounts.serializers import UserSerializer
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


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
