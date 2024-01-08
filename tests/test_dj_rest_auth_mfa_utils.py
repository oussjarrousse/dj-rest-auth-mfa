import pytest

from dj_rest_auth_mfa.adapters import DjangoMFA2Adapter
from dj_rest_auth_mfa.utils import __get_class__


@pytest.mark.UTILS
@pytest.mark.UNIT
def test___get_class__():

    class_name = "dj_rest_auth_mfa.adapters.DjangoMFA2Adapter"
    callable_class = __get_class__(class_name)
    instance = callable_class(None, None)
    assert isinstance(instance, object)
    assert isinstance(instance, DjangoMFA2Adapter)
