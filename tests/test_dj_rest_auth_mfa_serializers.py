import pyotp
import pytest
from django.contrib.auth.models import AnonymousUser
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from dj_rest_auth_mfa.serializers import MFALoginSerializer
from tests.conftest import create_mfa_entries
from tests.conftest import create_user


class Tests_MFALoginSerializer:
    @pytest.mark.django_db
    @pytest.mark.UNIT
    def test_mfa_authenticate(self, unauthenticated_api_client):
        username = "user"
        password = "password123_"
        email = "user@email.com"
        user = create_user(username, password, False, email)
        create_mfa_entries(username=username)
        totp = pyotp.TOTP("IAO2QZ5ZWI4V4JSG3P22I4FOOU5T73HF")

        factory = APIRequestFactory()
        totp_token = totp.now()
        request = factory.get("/api/v1/core/info/", {"token": totp_token})
        # force_authenticate(request, user)
        # unauthenticated_api_client.force_login(user)
        client = unauthenticated_api_client
        setattr(request, "session", client.session)
        serializer = MFALoginSerializer(context={"request": request})
        ret = serializer.mfa_authenticate(user)
        assert ret == user

        request = factory.post(
            "/api/v1/core/info/", {"token": "asdasdljslkajsdlkajsdlj"}
        )
        setattr(request, "session", client.session)
        serializer = MFALoginSerializer(context={"request": request})
        ret = serializer.mfa_authenticate(user)
        assert ret is None

        user = AnonymousUser()
        ret = serializer.mfa_authenticate(user)
        assert ret == user
        assert not ret.is_authenticated

    @pytest.mark.UNIT
    @pytest.mark.django_db
    def test__validate_username_email(self, unauthenticated_api_client):
        username = "user"
        password = "password123_"
        email = "user@email.com"
        user = create_user(username, password, False, email)
        create_mfa_entries(username=username)
        totp = pyotp.TOTP("IAO2QZ5ZWI4V4JSG3P22I4FOOU5T73HF")

        factory = APIRequestFactory()
        totp_token = totp.now()
        request = factory.post("/api/v1/core/info/", {"token": totp_token})
        # force_authenticate(request, user)
        # unauthenticated_api_client.force_login(user)
        client = unauthenticated_api_client
        setattr(request, "session", client.session)
        serializer = MFALoginSerializer(context={"request": request})

        # email and password
        ret = serializer._validate_username_email(username, None, password)
        assert ret == user
