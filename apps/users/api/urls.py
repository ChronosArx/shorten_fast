from django.urls import path

from .views import Register, CustomTokenObtainPairView, CustomTokenRefreshView

urlpatterns = [
    path("auth/register/", Register.as_view(), name="api_register"),
    path(
        "auth/login/", CustomTokenObtainPairView.as_view(), name="api_token_obtain_pair"
    ),
    path("auth/refresh/", CustomTokenRefreshView.as_view(), name="api_token_refresh"),
]
