import datetime
import logging
from abc import ABC
from abc import abstractmethod

from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError
from icecream import ic
from mfa.models import User_Keys

from .serializers import UserKeysSerializer

logger = logging.getLogger(__name__)


class MFAAdapter(ABC, object):
    @staticmethod
    @abstractmethod
    def methods():
        return []

    @staticmethod
    @abstractmethod
    def get_model_class():
        return object

    @staticmethod
    @abstractmethod
    def get_serializer_class():
        return object


DJANGO_MFA2_ADAPTER_SUPPORTED_METHODS = [
    # "U2F",
    # "FIDO2",
    "TOTP",
    # "Trusted_Devices",
    # "Email",
    "RECOVERY",
]


class DjangoMFA2Adapter(MFAAdapter):
    def __init__(self, request, user):
        self.request = request
        self.user = user

    def get_queryset(self, *argsv, **kwargs):
        queryset = self.get_model_class().objects.filter(username=self.user.username)
        return queryset

    def get_serializer_class(self):
        return UserKeysSerializer

    def authenticate(self):
        # ic(request.user.username)
        username = self.user.username
        uks = self.get_model_class().objects.filter(username=username, enabled=True)
        ic(uks)
        ic(uks.count())
        if uks.count() == 0:
            if settings.MFA_MANDATORY:
                # get user creation date
                # test = now() - user_creation_date < settings.MFA_GRACE_WINDOW_DAYS:
                test = (
                    datetime.datetime.urcnow() - self.user.created
                    < datetime.timedelta(days=settings.MFA_GRACE_WINDOW_DAYS)
                )
                if test:
                    return self.user
                else:
                    return self.force_logout()
            else:
                return self.user
        # loop over enabled mfa methods of the user
        mfa_methods = list(set([uk.key_type for uk in uks]))

        # this seems to be important for django_mfa2
        self.request.session["mfa_methods"] = mfa_methods

        for uk in uks:
            ic(uk.key_type)
            # check if the request has a key that would work with the key type
            # TOTP
            # RECOVERY
            adapter = self.methods_classes_map(uk.key_type)(self.request, self.user)
            token = self.request.POST["token"]
            r = adapter.verify_login(token)
            if r is True:
                return self.user

        return self.force_logout()

    def force_logout(self):
        # from django.contrib.auth import logout
        from dj_rest_auth.views import LogoutView

        view = LogoutView()
        response = view.logout(self.request)
        # logout(request) # should delete the session that was created by authenticate
        # ic(response)
        return None

    @staticmethod
    def methods():
        return DJANGO_MFA2_ADAPTER_SUPPORTED_METHODS

    @staticmethod
    def get_model_class():
        return User_Keys

    @staticmethod
    def methods_classes_map(key):
        from .recovery.adapters import RecoveryDjangoMFA2Adapter
        from .totp.adapters import TOTPDjangoMFA2Adapter

        the_map = {"RECOVERY": RecoveryDjangoMFA2Adapter, "TOTP": TOTPDjangoMFA2Adapter}
        return the_map[key]
