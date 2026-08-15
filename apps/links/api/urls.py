from rest_framework.routers import DefaultRouter
from .views import ShortLinkViewSet


router = DefaultRouter()
router.register("links", ShortLinkViewSet, basename="shortlink")

urlpatterns = router.urls
