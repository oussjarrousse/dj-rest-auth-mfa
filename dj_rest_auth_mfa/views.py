import logging

from django.conf import settings
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .utils import __get_class__

# from mfa.models import User_Keys

# from .adapters import DjangoMFA2Adapter
# from .serializers import UserKeysSerializer

logger = logging.getLogger(__name__)


class MFAViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    # serializer_class = UserKeysSerializer
    adapter_class = __get_class__(settings.MFA_ADAPTER_CLASS)
    # model = User_Keys

    def get_serializer_class(self):
        adapter = self.adapter_class(self.request, self.request.user)
        return adapter.get_serializer_class()

    def get_queryset(self, *argv, **kwargs):
        username = self.request.user.username
        #     # print(username)
        #     # queryset = User_Keys.objects.all()
        adapter = self.adapter_class(self.request, self.request.user)
        return adapter.get_queryset(*argv, **kwargs)

    @action(
        detail=False,
        methods=["get"],
        url_path="enabled",
        permission_classes=[IsAuthenticated],
    )
    def enabled(self, request, *args, **kwargs):
        """
        An API endpoint that accepts GET requests from authenticated users
        It returns a list of enabled mfa methods for the authenticated user
        """
        logger.info("MFAViewSet.enabled():")

        queryset = self.get_queryset().filter(enabled=True)

        mfa_enabled_methods = [x.key_type for x in queryset]
        logger.info(mfa_enabled_methods)
        return Response(data={"methods": mfa_enabled_methods})

    @action(
        detail=False,
        methods=["get"],
        url_path="methods",
        permission_classes=[AllowAny],
    )
    def methods(self, request, *args, **kwargs):
        logger.info("MFAViewSet.methods():")

        mfa_allowed_methods = [
            x
            for x in self.adapter_class.methods()
            if x not in settings.MFA_UNALLOWED_METHODS
        ]
        logger.info(mfa_allowed_methods)
        return Response(data={"methods": mfa_allowed_methods})
