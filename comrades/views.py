from django.contrib import auth
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from comrades.models import CustomUser
from comrades.serializers import RegistrationSerializer
from django.conf import settings
from django.contrib.auth import login, logout


class Registration(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            webtoken = default_token_generator.make_token(user=serializer.user)
            activation_link = f"http://127.0.0.1:8000/comrades/activation/{webtoken}"
            if serializer.user is not None:
                send_mail(
                    'Hello from eventmaster! To complete registration follow the link below.',
                    f'Activation link:  {activation_link}',
                    settings.EMAIL_HOST_USER,
                    [serializer.user.email]
                )
                return Response(
                    serializer.validated_data,
                    status=status.HTTP_201_CREATED
                )
            # пока что пользователь сохраняется и потом мешает, даже если письмо не прошло
        return Response(
            serializer.error_messages,
            status=status.HTTP_400_BAD_REQUEST
        )


class Activation(APIView):
    def post(self, request, webtoken):
        try:
            login_name = request.data['login']
        except KeyError:
            return Response("Invalid fieldnames", status=status.HTTP_400_BAD_REQUEST)
        try:
            user = CustomUser.objects.filter(email=login_name)[0]
            if user is not None and default_token_generator.check_token(user, webtoken):
                user.is_active = True
                user.save()
                return Response("Registration by email completed successfully", status=status.HTTP_202_ACCEPTED)
        except IndexError:
            try:
                user = CustomUser.objects.filter(username=login_name)[0]
                print(user.email)
                if user is not None and default_token_generator.check_token(user, webtoken):
                    user.is_active = True
                    user.save()
                    return Response("Registration by username completed successfully", status=status.HTTP_202_ACCEPTED)
            except IndexError:
                return Response("This email address does not registered", status=status.HTTP_400_BAD_REQUEST)
        return Response("Invalid data", status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(APIView):
    def post(self, request):
        login_name = request.data['login']
        password = request.data['password']
        try:
            user = auth.authenticate(
                request,
                email=login_name,
                password=password
                )
            if user is not None:
                login(request, user)
                token, flag = Token.objects.get_or_create(user=user)
                send_mail(
                    'Hello from eventmaster! Here is your access token ',
                    f'Token:  {token}',
                    settings.EMAIL_HOST_USER,
                    [user.email]
                )
                return Response("You are +", status=status.HTTP_200_OK)

            email = CustomUser.objects.filter(username=login_name)[0].email
            user = auth.authenticate(
                request,
                email=email,
                password=request.data['password']
            )
            if user is not None:
                login(request, user)
                token, flag = Token.objects.get_or_create(user=user)
                send_mail(
                    'Hello from eventmaster! Here is your access token ',
                    f'Token:  {token}',
                    settings.EMAIL_HOST_USER,
                    [user.email]
                )
                return Response({}, status=status.HTTP_200_OK)
        except KeyError:
            return Response("Invalid fieldnames", status=status.HTTP_400_BAD_REQUEST)
        return Response(
            "Invalid login or password, or account does not activated",
            status=status.HTTP_400_BAD_REQUEST
        )


class LogoutAPI(APIView):
    def post(self, request):
        logout(request)
        return Response({}, status=status.HTTP_200_OK)


