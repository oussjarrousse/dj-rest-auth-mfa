from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import RecoveryViewSet

# from .views import RecoverySetupView
# from .views import RecoveryVerify

router = DefaultRouter()
router.register(r"", RecoveryViewSet, basename="mfa_recovery")

# urlpatterns = router.urls
urlpatterns = [
    path("", include(router.urls)),
]
