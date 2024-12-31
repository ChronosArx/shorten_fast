from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView
from shorten.api.views import Redirects
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("shorten.api.urls")),
    path("api/", include("authentication.api.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("<str:code>", Redirects.as_view(), name="redirects"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
