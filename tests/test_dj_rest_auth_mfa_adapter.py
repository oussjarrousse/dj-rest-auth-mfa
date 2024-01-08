import pyotp
import pytest
from django.conf import settings
from django.db.models import QuerySet
from mfa.models import User_Keys
from rest_framework.test import APIRequestFactory

from dj_rest_auth_mfa.adapters import DJANGO_MFA2_ADAPTER_SUPPORTED_METHODS
from dj_rest_auth_mfa.adapters import DjangoMFA2Adapter
from dj_rest_auth_mfa.adapters import MFAAdapter
from dj_rest_auth_mfa.recovery.adapters import RecoveryDjangoMFA2Adapter
from dj_rest_auth_mfa.totp.adapters import TOTPDjangoMFA2Adapter
from tests.conftest import create_mfa_entries
from tests.conftest import create_user

# from django.contrib.auth import authenticate


@pytest.mark.UTILS
def test_mfa_adapter_is_an_abstract_class():
    with pytest.raises(TypeError):
        django_mfa2_adapter = MFAAdapter()


class Tests_DjangoMFA2Adapter:
    @pytest.mark.UNIT
    def test_methods(self):
        django_mfa2_adapter = DjangoMFA2Adapter(None, None)
        ret = django_mfa2_adapter.methods()
        assert isinstance(ret, list)
        assert ret == DJANGO_MFA2_ADAPTER_SUPPORTED_METHODS

    @pytest.mark.UNIT
    def test_get_model_class(self):
        django_mfa2_adapter = DjangoMFA2Adapter(None, None)
        ret = django_mfa2_adapter.get_model_class()
        assert ret == User_Keys

    @pytest.mark.parametrize("key", DJANGO_MFA2_ADAPTER_SUPPORTED_METHODS)
    @pytest.mark.UNIT
    def test_methods_classes_map(self, key):
        the_map = {"RECOVERY": RecoveryDjangoMFA2Adapter, "TOTP": TOTPDjangoMFA2Adapter}
        django_mfa2_adapter = DjangoMFA2Adapter(None, None)
        ret = django_mfa2_adapter.methods_classes_map(key)
        assert ret == the_map[key]

    @pytest.mark.UNIT
    @pytest.mark.django_db
    def test_get_queryset(self):
        request = None
        user = create_user("user", "password123_", False)
        django_mfa2_adapter = DjangoMFA2Adapter(request, user)
        qs = django_mfa2_adapter.get_queryset()
        assert isinstance(qs, QuerySet)
        assert qs.count() == 0

    @pytest.mark.UNIT
    @pytest.mark.django_db
    def test_authenticate_mfa_is_not_setup(self):

        user = create_user("user", "password123_", False)

        # MFA_MANDATORY is False & no MFA is setup
        settings.MFA_MANDATORY = False
        django_mfa2_adapter = DjangoMFA2Adapter(None, user)
        ret = django_mfa2_adapter.authenticate()
        assert ret == user

        # MFA_MANDATORY is True & no MFA is setup
        # grace period and so on

    @pytest.mark.UNIT
    @pytest.mark.django_db
    def test_authenticate_mfa_is_setup(self, unauthenticated_api_client):
        username = "user"
        password = "password123_"
        user = create_user("user", "password123_", False)
        create_mfa_entries(user.username)

        unauthenticated_api_client.force_login(user)
        client = unauthenticated_api_client
        # MFA_MANDATORY is True or False & MFA is setup 2 methods
        # the request should have a session, etc.
        client.get("/api/v1/core/info/")

        factory = APIRequestFactory()
        request = factory.post(
            "/api/v1/core/info/", {"token": "NOT A GOOD TOKEN VALUE"}
        )
        setattr(request, "session", client.session)
        django_mfa2_adapter = DjangoMFA2Adapter(request, user)
        ret = django_mfa2_adapter.authenticate()
        assert not ret

        # testing recovery token
        request = factory.post("/api/v1/core/info/", {"token": "Zx1m1-9cNis"})
        django_mfa2_adapter.request = request
        setattr(request, "session", client.session)
        ret = django_mfa2_adapter.authenticate()
        assert ret == user

        # testing totp token
        totp = pyotp.TOTP("IAO2QZ5ZWI4V4JSG3P22I4FOOU5T73HF")
        totp_token = totp.now()
        request = factory.post("/api/v1/core/info/", {"token": totp_token})
        django_mfa2_adapter.request = request
        setattr(request, "session", client.session)
        ret = django_mfa2_adapter.authenticate()
        assert ret == user
