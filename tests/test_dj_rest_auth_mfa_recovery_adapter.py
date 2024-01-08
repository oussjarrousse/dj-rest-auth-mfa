import json

import pytest
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from dj_rest_auth_mfa.recovery.adapters import RecoveryDjangoMFA2Adapter
from tests.conftest import create_user


class Tests_RecoveryDjangoMFA2Adapter:
    @pytest.mark.UNIT
    @pytest.mark.django_db
    def test_get_tokens(self):
        username = "user"
        password = "password123_"
        user = create_user("user", "password123_", False)
        self.user = user
        factory = APIRequestFactory()
        request = factory.post("/api/v1/core/info/")
        # force_authenticate(request, user)
        setattr(request, "user", user)
        django_mfa2_recovery_adapter = RecoveryDjangoMFA2Adapter(request, user)
        r = django_mfa2_recovery_adapter.get_tokens()
        r = json.loads(r.content)
        assert isinstance(r, dict)
        assert "keys" in r
        assert isinstance(r["keys"], list)
        assert len(r["keys"]) == 5
        for item in r["keys"]:
            assert len(item) == 11
            assert item[5] == "-"
        self.tokens = r["keys"]

    @pytest.mark.UNIT
    @pytest.mark.django_db
    def test_complete_setup(self):
        self.test_get_tokens()
        factory = APIRequestFactory()
        request = factory.post("/api/v1/core/info/", {"token": self.tokens[0]})
        setattr(request, "user", self.user)
        django_mfa2_recovery_adapter = RecoveryDjangoMFA2Adapter(request, self.user)
        r = django_mfa2_recovery_adapter.complete_setup()
        assert r
