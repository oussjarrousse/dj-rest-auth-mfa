from django.conf import settings
from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import TOTPViewSet

# from mfa import totp

# from .views import TOTPSetupView
# from .views import TOTPVerifyView

router = DefaultRouter()
router.register(r"", TOTPViewSet, basename="mfa_totp")

urlpatterns = [
    path("", include(router.urls)),
]
