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
            user = serializer.instance

            webtoken = default_token_generator.make_token(user=user)
            activation_link = f"{settings.SITE_URL}/comrades/activation/{webtoken}"

            if user is not None:
                abs_uri = request.build_absolute_uri("")
                if abs_uri.find("test") != -1:
                    return Response(
                        {
                            "host_email": settings.EMAIL_HOST_USER,
                            "user_email": user.email,
                            "user": UserSerializer(user, context=self.get_serializer_context()).data,
                            "webtoken": webtoken,
                            "activation_link": activation_link,
                            "msg": "You have successfully registered. Check your email to complete registration.",
                        },
                        status=status.HTTP_201_CREATED
                    )

                send_mail(
                    'Hello from eventmaster! To complete registration follow by the link below.',
                    f'Activation link:  {activation_link}',
                    settings.EMAIL_HOST_USER,
                    [user.email]
                )
                return Response(
                    {
                        "user": UserSerializer(user, context=self.get_serializer_context()).data,
                        "msg": "You have successfully registered. Check your email to complete registration",
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
                return Response(
                    {"msg": "Registration by email completed successfully"},
                    status=status.HTTP_202_ACCEPTED
                )
        except IndexError:
            try:
                user = CustomUser.objects.filter(username=login_name)[0]
                if user is not None and default_token_generator.check_token(user, webtoken):
                    user.is_active = True
                    user.save()
                    return Response(
                        {"msg": "Registration by username completed successfully"},
                        status=status.HTTP_202_ACCEPTED
                    )
            except IndexError:
                return Response(
                    {"msg": "This user is not registered"}
                    , status=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            {"msg": "Invalid webtoken"},
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginAPI(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            login_name = serializer.data['login']
            password = serializer.data['password']
        try:
            abs_uri = request.build_absolute_uri("")
            user = auth.authenticate(
                request,
                email=login_name,
                password=password
                )
            if user is not None:
                login(request, user)
                token, flag = Token.objects.get_or_create(user=user)
                if abs_uri.find("test") != -1:
                    return Response(
                        {
                            "host_email": settings.EMAIL_HOST_USER,
                            "user_email": user.email,
                            "token": f"{token}",
                            "msg": "You have successfully logged in by email. Check your email to find token.",
                        },
                        status=status.HTTP_200_OK
                    )
                send_mail(
                    'Hello from eventmaster! Here is your access token.',
                    f'Token:  {token}',
                    settings.EMAIL_HOST_USER,
                    [user.email]
                )
                return Response(
                    {
                        "msg": "You have successfully logged in by email. Check your email to find token.",
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
                if abs_uri.find("test") != -1:
                    return Response(
                        {
                            "host_email": settings.EMAIL_HOST_USER,
                            "user_email": user.email,
                            "token": f"{token}",
                            "msg": "You have successfully logged in by username. Check your email to find token.",
                        },
                        status=status.HTTP_200_OK
                    )
                send_mail(
                    'Hello from eventmaster! Here is your access token.',
                    f'Token:  {token}',
                    settings.EMAIL_HOST_USER,
                    [user.email]
                )
                return Response(
                    {
                        "msg": "You have successfully logged in by username. Check your email to find token.",
                    },
                    status=status.HTTP_200_OK
                )
        except IndexError:
            return Response(
                {"msg": "This user does not exist (invalid login or password) or account is not activated."},
                status=status.HTTP_403_FORBIDDEN
            )
        return Response(
            {"msg": "Invalid password or account is not activated."},
            status=status.HTTP_403_FORBIDDEN
        )


class LogoutAPI(APIView):
    def post(self, request):
        logout(request)
        return Response({}, status=status.HTTP_200_OK)


