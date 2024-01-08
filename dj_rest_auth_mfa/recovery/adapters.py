import logging

from django.utils.datastructures import MultiValueDictKeyError
from icecream import ic
from mfa import recovery as mfa2_recovery
from mfa.models import User_Keys

from ..adapters import DjangoMFA2Adapter

logger = logging.getLogger(__name__)


class RecoveryDjangoMFA2Adapter(DjangoMFA2Adapter):
    def get_model(self):
        return User_Keys.objects.get(username=self.user.username, key_type="RECOVERY")

    def verify_login(self, token):
        try:
            result = mfa2_recovery.verify_login(self.request, self.user.username, token)
            if result[0] == True:
                return True
            return False
        except MultiValueDictKeyError:
            logger.error(
                "RecoveryDjangoMFA2Adapter.verify_login(): MultiValueDictKeyError"
            )
            return False
        except Exception:
            logger.error("RecoveryDjangoMFA2Adapter.verify_login(): Exception")
            return False

    def complete_setup(self):
        # check if the token is valid return True or False or raise Exception
        try:
            token = self.request.POST["token"]
            result = mfa2_recovery.verify_login(self.request, self.user.username, token)
            if result[0] == True:
                ic(result)
                # do some magic and set some variables in the adapter
                uk = self.get_model()
                uk.enabled = True
                uk.save()
                return True
            return False
        except MultiValueDictKeyError:
            logger.error(
                "RecoveryDjangoMFA2Adapter.complete_setup(): MultiValueDictKeyError"
            )
            return False
        except Exception:
            logger.error("RecoveryDjangoMFA2Adapter.complete_setup(): Exception")
            return False

    def get_tokens(self):
        r = mfa2_recovery.genTokens(self.request)
        # TODO
        uk = self.get_model()
        uk.enabled = False
        uk.save()
        return r
