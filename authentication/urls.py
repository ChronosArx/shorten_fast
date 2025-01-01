from django.urls import path
from .views import Register, LogIn, LogOut, GenerateAccessToken, CheckAuth

urlpatterns = [
    path("auth/register/", Register.as_view(), name="register"),
    path("auth/login/", LogIn.as_view(), name="login"),
    path("auth/logout/", LogOut.as_view(), name="logout"),
    path(
        "auth/new_access_token/", GenerateAccessToken.as_view(), name="new_access_token"
    ),
    path("auth/check_auth", CheckAuth.as_view(), name="check_auth"),
    # path("auth/confirm_email/", ConfirmEmail.as_view(), name="confirm_email"),
]
