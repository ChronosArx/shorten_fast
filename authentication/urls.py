from django.urls import path
from .views import Register, LogIn, LogOut, GenerateAccesToken

urlpatterns = [
    path("auth/register/", Register.as_view(), name="register"),
    path("auth/login/", LogIn.as_view(), name="login"),
    path("auth/logout/", LogOut.as_view(), name="logout"),
    path(
        "auth/new_access_token", GenerateAccesToken.as_view(), name="new_access_token"
    ),
]
