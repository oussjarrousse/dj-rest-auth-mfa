# dj-rest-auth-mfa

## Overview

`dj-rest-auth-mfa` is a Django App that is actually a plugin for the `dj-rest-auth`. It adds RESTful API endpoints that adds multifactor authentication (MFA) support to accounts by using the `django-mfa2` package.

## Requirements:

Besides Django, this package depends on the following projects:
- [django-allauth](https://allauth.org/) that provides advanced authentication functionality to the Django framework.
- [django-rest-framework](https://django-rest-framework.org), DRF, that provides an extendible and flexible way to build Web APIs on top of Django
- [dj-rest-auth](https://dj-rest-auth.readthedocs.io/en/latest/introduction.html) provides RESTful API endpoints for the django-allauth using DRF (`django-allauth` does not provide API support out of the box [yet](https://allauth.org/news/2024/04/api-feedback/).)
- [django-mfa2](https://github.com/mkalioby/django-mfa2) which is a Django app that adds supports for TOTP, U2F, FIDO2 U2F (Web Authn), Email Tokens, Trusted Devices, backup codes, and Passkeys. (`django-allauth` only supports TOTP out of the box.)

To use the package effectively, make sure `django-allauth`, `django-rest-framework`, `dj-rest-auth` and `django-mfa2` are installed and configured correctly.

## Installation

To install `dj-rest-auth-mfa` run:

```bash
pip install dj-rest-auth-mfa
```

In the settings.py you should have the following:

```pytest
INSTALLED_APPS = [
    # ...
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.sites",
    # ...
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "mfa",  # this is django-mfa2
    "allauth",  # this is django-allauth
    "dj_rest_auth", # this is dj-rest-auth
    "dj_rest_auth_mfa"  # this package
]

# https://docs.djangoproject.com/en/4.2/ref/contrib/sites/
SITE_ID = 1

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware", # this is important for allauth
]

```

## Configurations:

beside the configurations required by django-allauth and those required by dj-rest-auth, 
and the configurations necessary for django-mfa2, there are the following configurations that should be defined in the django settings.py file:

```python
RECOVERY_ITERATION = 720000   # this is the recommended value for hashing iterations
MFA_MANDATORY = False
MFA_ADAPTER_CLASS = "dj_rest_auth_mfa.adapters.DjangoMFA2Adapter"
MFA_GRACE_WINDOW_DAYS = 7
```

## Features

Currently only the following methods are supported

```python
MFA_UNALLOWED_METHODS = [
  "RECOVERY",
  "TOTP
]
```

## Integration

Ones installed and configured, the package provides the following API nodes:

```
/totp/
/totp/setup
/totp/verify

/recovery/
/recovery/setup
/recovery/verify
```

## Contributing
Contributions to this project are welcomed! The Contributing Guide is still under construction.

When creating a pull request make sure to use the following template:

```
Change Summary
 - item one
 - item two
Related issue number
 - issue a
 - issue b
Checklist
  [ ] code is ready
  [ ] add tests
  [ ] all tests passing
  [ ] test coverage did not drop
  [ ] PR is ready for review
```

## License
dj-rest-auth-saml is licensed under the MIT License - see the LICENSE file for details.
