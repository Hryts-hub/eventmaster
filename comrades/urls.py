from django.urls import path

from comrades.views import CreateToken, Registration, Activation

urlpatterns = [
    path("create_token/", CreateToken.as_view(), name='create_token'),
    path("registration/", Registration.as_view(), name='registration'),
    path("activation/<str:webtoken>", Activation.as_view(), name='activation'),
]