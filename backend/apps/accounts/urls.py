from django.urls import path

from .views import Register, CustomTokenObtainPairView, CustomTokenRefreshView

app_name = "users"

urlpatterns = [
    path("auth/register/", Register.as_view(), name="register"),
    path("auth/login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
]
