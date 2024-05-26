from accounts.auth import Authentication
from accounts.serializers import UserSerializer
from rest_framework import status
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
