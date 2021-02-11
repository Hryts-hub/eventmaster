from django.contrib import auth
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from comrades.models import CustomUser
from comrades.serializers import RegistrationSerializer, UserSerializer, ActivationSerializer, LoginSerializer
from django.conf import settings
from django.contrib.auth import login, logout, authenticate


class Registration(GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            webtoken = default_token_generator.make_token(user=serializer.user)

            activation_link = f"https://blackdesert.ololosha.xyz/comrades/activation/{webtoken}"

            # activation_link = f"http://127.0.0.1:8000/comrades/activation/{webtoken}"
            # request.build_absolute_uri("") --> http://127.0.0.1:8000/comrades/registration/ <-- even on prod

            if serializer.user is not None:
                send_mail(
                    'Hello from eventmaster! To complete registration follow the link below.',
                    f'Activation link:  {activation_link}',
                    settings.EMAIL_HOST_USER,
                    [serializer.user.email]
                )
                user = serializer.user
                # webtoken and activation_link in Response for testing
                # (They may be excluded from Response, and test_activation must be commented out) -
                # activation will work properly
                return Response(
                    {
                        "user": UserSerializer(user, context=self.get_serializer_context()).data,
                        "webtoken": webtoken,
                        "activation_link": activation_link
                    },
                    status=status.HTTP_201_CREATED
                )
        return Response(
            serializer.error_messages,
            status=status.HTTP_400_BAD_REQUEST
        )


class Activation(GenericAPIView):
    serializer_class = ActivationSerializer

    def post(self, request, webtoken):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            login_name = serializer.data['login']

        try:
            user = CustomUser.objects.filter(email=login_name)[0]
            if user is not None and default_token_generator.check_token(user, webtoken):
                user.is_active = True
                user.save()
                return Response("Registration by email completed successfully", status=status.HTTP_202_ACCEPTED)
        except IndexError:
            try:
                user = CustomUser.objects.filter(username=login_name)[0]
                if user is not None and default_token_generator.check_token(user, webtoken):
                    user.is_active = True
                    user.save()
                    return Response("Registration by username completed successfully", status=status.HTTP_202_ACCEPTED)
            except IndexError:
                return Response("This user is not registered", status=status.HTTP_400_BAD_REQUEST)
        return Response("Invalid webtoken", status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            login_name = serializer.data['login']
            password = serializer.data['password']

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
                # token in Response only for convenience, but don't need.
                # It can be replaced easily by some other message.
                return Response(
                    {
                        "token": f"{token}",
                        "msg": "Login by email",
                    },
                    status=status.HTTP_200_OK
                )

            email = CustomUser.objects.filter(username=login_name)[0].email
            user = authenticate(
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
                return Response(
                    {
                        "token": f"{token}",
                        "msg": "Login by username",
                    },
                    status=status.HTTP_200_OK
                )
        except IndexError:
            return Response("The user does not exist", status=status.HTTP_403_FORBIDDEN)
        return Response(
            "Invalid password or account is not activated",
            status=status.HTTP_400_BAD_REQUEST
        )


class LogoutAPI(APIView):
    def post(self, request):
        logout(request)
        return Response({}, status=status.HTTP_200_OK)


