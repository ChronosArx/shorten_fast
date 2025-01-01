from rest_framework.routers import DefaultRouter
from .viewsets import ShortLinkViewSet

router = DefaultRouter()
router.register("shorten", ShortLinkViewSet, basename="shortlink")

urlpatterns = router.urls
