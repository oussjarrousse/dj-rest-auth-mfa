from dj_rest_auth.serializers import LoginSerializer
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from icecream import ic
from mfa.models import User_Keys
from rest_framework import exceptions
from rest_framework import serializers

from .utils import __get_class__

# from .adapters import MFAAdapter
# from .adapters import DjangoMFA2Adapter
# from .adapters import RecoveryDjangoMFA2Adapter
# from .adapters import TOTPDjangoMFA2Adapter


class UserKeysSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Keys
        fields = "__all__"
        # read_only_fields = ['username']

    # username = serializers.CharField(max_length=50)
    # properties = serializers.JSONField(allow_null=True)
    # added_on = serializers.DateTimeField(read_only=True)
    # key_type = serializers.CharField(max_length=25, default="TOTP")
    # enabled = serializers.BooleanField(default=True)
    # expires = serializers.DateTimeField(allow_null=True, default=None)
    # last_user = serializers.DateTimeField(allow_null=True, default=None)
    # owned_by_enterprise = serializers.BooleanField(allow_null=True, default=None)


class MFALoginSerializer(LoginSerializer):
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={"input_type": "password"})
    token = serializers.CharField(required=False, allow_blank=True)
    # def authenticate(self, **kwargs):
    # return authenticate(self.context['request'], **kwargs)

    def _validate_email(self, email, password):
        if email and password:
            user = self.authenticate(email=email, password=password)
        else:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

        if not user.is_authenticated or not user.is_active:
            return user

        # now do the mfa magic
        user = self.mfa_authenticate(user)

        return user

    def _validate_username(self, username, password):
        if username and password:
            user = self.authenticate(username=username, password=password)
        else:
            msg = _('Must include "username" and "password".')
            raise exceptions.ValidationError(msg)

        if not user.is_authenticated or not user.is_active:
            return user

        user = self.mfa_authenticate(user)

        return user

    def _validate_username_email(self, username, email, password):
        if email and password:
            return self._validate_email(email=email, password=password)
            # user = self.authenticate(email=email, password=password)

        if username and password:
            return self._validate_username(username=username, password=password)
            # user = self.authenticate(username=username, password=password)

        msg = _('Must include either "username" or "email" and "password".')
        raise exceptions.ValidationError(msg)

        #  def login(request): # this function handles the login form POST
        #     user = auth.authenticate(username=username, password=password)
        #     if user is not None: # if the user object exist
        #          from mfa.helpers import has_mfa
        #          res =  has_mfa(username = username,request=request) # has_mfa returns false or HttpResponseRedirect
        #          if res:
        #              return res
        #          return log_user_in(request,username=user.username)
        #          #log_user_in is a function that handles creatung user session, it should be in the setting file as MFA_CALLBACK

        # return user

    def get_auth_user_using_allauth(self, username, email, password):
        from allauth.account import app_settings as allauth_account_settings

        # Authentication through email
        if (
            allauth_account_settings.AUTHENTICATION_METHOD
            == allauth_account_settings.AuthenticationMethod.EMAIL
        ):
            return self._validate_email(email, password)

        # Authentication through username
        if (
            allauth_account_settings.AUTHENTICATION_METHOD
            == allauth_account_settings.AuthenticationMethod.USERNAME
        ):
            return self._validate_username(username, password)

        # Authentication through either username or email
        return self._validate_username_email(username, email, password)

    # def get_auth_user_using_orm(self, username, email, password):
    #     if email:
    #         try:
    #             username = UserModel.objects.get(email__iexact=email).get_username()
    #         except UserModel.DoesNotExist:
    #             pass

    #     if username:
    #         return self._validate_username_email(username, '', password)

    #     return None

    # def get_auth_user(self, username, email, password):
    #     """
    #     Retrieve the auth user from given POST payload by using
    #     either `allauth` auth scheme or bare Django auth scheme.

    #     Returns the authenticated user instance if credentials are correct,
    #     else `None` will be returned
    #     """
    #     if 'allauth' in settings.INSTALLED_APPS:

    #         # When `is_active` of a user is set to False, allauth tries to return template html
    #         # which does not exist. This is the solution for it. See issue #264.
    #         try:
    #             return self.get_auth_user_using_allauth(username, email, password)
    #         except url_exceptions.NoReverseMatch:
    #             msg = _('Unable to log in with provided credentials.')
    #             raise exceptions.ValidationError(msg)
    #     return self.get_auth_user_using_orm(username, email, password)

    # @staticmethod
    # def validate_auth_user_status(user):
    #     if not user.is_active:
    #         msg = _('User account is disabled.')
    #         raise exceptions.ValidationError(msg)

    # @staticmethod
    # def validate_email_verification_status(user, email=None):
    #     from allauth.account import app_settings as allauth_account_settings
    #     if (
    #         allauth_account_settings.EMAIL_VERIFICATION == allauth_account_settings.EmailVerificationMethod.MANDATORY
    #         and not user.emailaddress_set.filter(email=user.email, verified=True).exists()
    #     ):
    #         raise serializers.ValidationError(_('E-mail is not verified.'))

    # def validate(self, attrs):
    #     username = attrs.get('username')
    #     email = attrs.get('email')
    #     password = attrs.get('password')
    #     user = self.get_auth_user(username, email, password)

    #     if not user:
    #         msg = _('Unable to log in with provided credentials.')
    #         raise exceptions.ValidationError(msg)

    #     # Did we get back an active user?
    #     self.validate_auth_user_status(user)

    #     # If required, is the email verified?
    #     if 'dj_rest_auth.registration' in settings.INSTALLED_APPS:
    #         self.validate_email_verification_status(user, email=email)

    #     attrs['user'] = user
    #     return attrs
    def mfa_authenticate(self, user):
        if not user.is_authenticated or not user.is_active:
            return user

        # TODO: MOVE THESE TO AN ADAPTER
        request = self.context.get("request")
        adapter_class = __get_class__(settings.MFA_ADAPTER_CLASS)
        adapter = adapter_class(request, user)
        user = adapter.authenticate()
        return user
