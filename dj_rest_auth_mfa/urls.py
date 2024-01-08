from django.conf import settings
from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .recovery import urls as recovery_urls
from .totp import urls as totp_urls
from .views import MFAViewSet

router = DefaultRouter()
router.register("", MFAViewSet, basename="mfa")

urlpatterns = [
    # path(
    #     "auth/mfa/",
    #     include(
    #         [
    path("totp/", include(totp_urls.urlpatterns)),
    path("recovery/", include(recovery_urls.urlpatterns)),
    path("", include(router.urls)),
    #         ]
    #     ),
    # ),
]
