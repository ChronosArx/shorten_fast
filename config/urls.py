from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

from apps.links.api.views import Redirects


urlpatterns = [
    # Urls redirect
    path("<str:code>", Redirects.as_view(), name="redirects"),
    # Urls Admin
    path("admin/", admin.site.urls),
    # Urls for API
    path("api/", include("apps.links.api.urls")),
    path("api/", include("apps.users.api.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]

if settings.DEBUG:
    urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
