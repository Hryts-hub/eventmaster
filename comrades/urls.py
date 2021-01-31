from django.urls import path

from comrades.views import Registration, Activation, LoginAPI, LogoutAPI

urlpatterns = [
    path("registration/", Registration.as_view(), name='registration'),
    path("activation/<str:webtoken>", Activation.as_view(), name='activation'),
    path("login/", LoginAPI.as_view(), name='login'),
    path("logout/", LogoutAPI.as_view(), name='logout'),
]