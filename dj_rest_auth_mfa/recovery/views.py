import json
import logging

from icecream import ic
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_202_ACCEPTED
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.viewsets import ModelViewSet

from ..serializers import UserKeysSerializer
from .adapters import RecoveryDjangoMFA2Adapter
from .serializers import RecoverySerializer

logger = logging.getLogger(__name__)


class RecoveryViewSet(ModelViewSet):
    serializer_class = UserKeysSerializer
    model = RecoveryDjangoMFA2Adapter.get_model_class()
    throttle_scope = "dj_rest_auth"
    adapter_class = RecoveryDjangoMFA2Adapter
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *argv, **kwargs):
        username = self.request.user.username
        queryset = self.model.objects.filter(
            username=self.request.user.username, key_type="RECOVERY"
        )
        return queryset

    @action(
        detail=False,
        methods=["get"],
        url_path="setup",
        serializer_class=RecoverySerializer,
        permission_classes=[IsAuthenticated],
    )
    def setup(self, request, *args, **kwargs):
        logger.info("RecoveryViewSet.setup()")
        # will delete old backup codes
        # and generate new tokens
        # and store after salting and hashing with iterations
        # and return the 5 tokens
        adapter = self.adapter_class(self.request, self.request.user)
        r = adapter.get_tokens()
        # will make sure they are not enabled unless
        # a post with a correct token has been sent
        # that means only 4 active backup codes remains
        return Response(json.loads(r.content))

    @setup.mapping.post
    def setup_post(self, request, *args, **kwargs):
        logger.info("RecoveryViewSet.activate()")
        recovery_serializer = self.serializer_class(data=request.data)
        # recovery_serializer = RecoverySerializer(data=request.data)
        adapter = self.adapter_class(request, request.user)
        if recovery_serializer.is_valid():
            # token = recovery_serializer.validated_data["token"]
            result = adapter.complete_setup()
            if result is True:
                return Response(
                    {"message": "backup tokens activated"}, status=HTTP_202_ACCEPTED
                )

            return Response(
                {"message": "token is not valid"}, status=HTTP_401_UNAUTHORIZED
            )

        return Response(recovery_serializer.errors, status=HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["post"],
        url_path="verify",
        permission_classes=[AllowAny],
        serializer_class=RecoverySerializer,
    )
    def verify(self, request, *args, **kwargs):
        logger.info("RecoveryViewSet.verify()")
        token = request.POST["token"]
        recovery_serializer = self.serializer_class(data=request.data)
        if recovery_serializer.is_valid():
            token = recovery_serializer.validated_data["token"]
            adapter = self.adapter_class(request, request.user)
            result = adapter.verify_login(token)
            if result is True:
                # check if it is the last token...
                ic("authenticate")
                return Response({"message": "token accepted"}, status=HTTP_202_ACCEPTED)
            return Response(
                {"message": "token is not valid"}, status=HTTP_401_UNAUTHORIZED
            )
        return Response(recovery_serializer.errors, status=HTTP_400_BAD_REQUEST)
