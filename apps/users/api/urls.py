from django.urls import path

from .views import Register, CustomTokenObtainPairView, CustomTokenRefreshView

app_name = "api"

urlpatterns = [
    path("auth/register/", Register.as_view(), name="user_register"),
    path("auth/login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
]
