from django.contrib import auth
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from comrades.serializers import RegistrationSerializer
from django.conf import settings


class CreateToken(APIView):
    def post(self, request):
        login = request.data.get('login')
        pwd = request.data.get("pwd")
        user = auth.authenticate(request, username=login, password=pwd)
        if user is not None:
            token, flag = Token.objects.get_or_create(user=user)
            return Response({"token": token.__str__()}, status=status.HTTP_201_CREATED)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


class Registration(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # token получаем по урлу (см jupiter)

            webtoken = default_token_generator.make_token(user=serializer.user)
            if serializer.user is not None:
                # test mail without url
                send_mail(
                    'hello ',
                    f'test {webtoken}',
                    settings.EMAIL_HOST_USER,
                    [serializer.user.email]
                )
            return Response(
                serializer.validated_data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.error_messages,
            status=status.HTTP_400_BAD_REQUEST
        )

