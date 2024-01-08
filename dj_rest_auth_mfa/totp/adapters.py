import logging

from django.utils.datastructures import MultiValueDictKeyError
from icecream import ic
from mfa import totp as mfa2_totp
from mfa.models import User_Keys

from ..adapters import DjangoMFA2Adapter

logger = logging.getLogger(__name__)


class TOTPDjangoMFA2Adapter(DjangoMFA2Adapter):
    def get_model(self):
        return User_Keys.objects.get(username=self.user.username, key_type="TOTP")

    def verify_login(self, token):
        try:
            result = mfa2_totp.verify_login(None, self.user, token)
            if result[0] == True:
                return True
            return False
        except MultiValueDictKeyError:
            logger.error("TOTPDjangoMFA2Adapter.verify_login(): MultiValueDictKeyError")
            return False
        except Exception:
            logger.error("TOTPDjangoMFA2Adapter.verify_login(): Exception")
            return False

    def complete_setup(self):
        # check if the token is valid return True or False or raise Exception
        try:
            # pass
            token = self.request.POST["token"]
            key = self.request.POST["key"]
            mutable_backup = self.request.GET._mutable
            self.request.GET._mutable = True
            self.request.GET["answer"] = token
            self.request.GET["key"] = key
            self.request.GET._mutable = mutable_backup
            result = mfa2_totp.verify(self.request)
            ic(result)
            if result.content.decode("utf-8") == "Success":
                return True
            return False
        except MultiValueDictKeyError as e:
            logger.error(
                "TOTPDjangoMFA2Adapter.complete_setup(): MultiValueDictKeyError"
            )
            logger.error(e)
            return False
        except Exception as e:
            logger.error("TOTPDjangoMFA2Adapter.complete_setup(): Exception")
            logger.error(e)
            return False

    def get_tokens(self):
        # check if recovery codes are setup
        #
        # delete old totp
        #
        r = mfa2_totp.getToken(self.request)
        return r
