from django.urls import path

from comrades.views import CreateToken, Registration

urlpatterns = [
    path("create_token/", CreateToken.as_view()),
    path("registration/", Registration.as_view()),
]