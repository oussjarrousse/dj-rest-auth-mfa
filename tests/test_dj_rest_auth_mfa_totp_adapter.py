import json

import pyotp
import pytest
from django.conf import settings
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from dj_rest_auth_mfa.totp.adapters import TOTPDjangoMFA2Adapter
from tests.conftest import create_user


class Tests_TOTPDjangoMFA2Adapter:
    @pytest.mark.UNIT
    @pytest.mark.FOCUS
    @pytest.mark.django_db
    def test_get_tokens(self, unauthenticated_api_client):
        username = "user"
        password = "password123_"
        user = create_user("user", "password123_", False)
        self.user = user
        factory = APIRequestFactory()
        request = factory.post("/api/v1/core/info/")
        # force_authenticate(request, user)
        unauthenticated_api_client.force_login(user)
        client = unauthenticated_api_client

        setattr(request, "user", user)
        setattr(request, "session", client.session)
        django_mfa2_totp_adapter = TOTPDjangoMFA2Adapter(request, user)
        r = django_mfa2_totp_adapter.get_tokens()
        r = json.loads(r.content)
        assert isinstance(r, dict)
        assert "qr" in r
        assert "secret_key" in r
        assert isinstance(r["secret_key"], str)
        assert len(r["secret_key"]) == 32
        self.secret_key = r["secret_key"]

    @pytest.mark.UNIT
    @pytest.mark.FOCUS
    @pytest.mark.django_db
    def test_complete_setup(self, unauthenticated_api_client):
        self.test_get_tokens(unauthenticated_api_client)
        factory = APIRequestFactory()
        totp = pyotp.TOTP(self.secret_key)
        totp_token = totp.now()
        request = factory.post(
            "/api/v1/core/info/", {"token": totp_token, "key": self.secret_key}
        )
        unauthenticated_api_client.force_login(self.user)
        client = unauthenticated_api_client
        setattr(request, "user", self.user)
        setattr(request, "session", client.session)
        django_mfa2_totp_adapter = TOTPDjangoMFA2Adapter(request, self.user)
        r = django_mfa2_totp_adapter.complete_setup()
        assert not r

        settings.MFA_ENFORCE_RECOVERY_METHOD = False
        r = django_mfa2_totp_adapter.complete_setup()
        assert r
