# dj-rest-auth-mfa

## Overview

`dj-rest-auth-mfa` is a Django App that is actually a plugin for the `dj-rest-auth` that adds mfa support to email/username accounts, by using the `django-mfa2` package.

## Requirements:

Make sure the requirements for `django-allauth`, `dj-rest-auth` and `django-mfa2` are met

## Installation

To install `dj-rest-auth-mfa ` run:

```bash
pip install dj-rest-auth-mfa
```

In the settings.py you should have the following:

```pytest
INSTALLED_APPS = [
    # ...
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "mfa",  # this is django-mfa2
    "allauth",  # this is django-allauth
    "dj_rest_auth", # this is dj-rest-auth
    "dj_rest_auth_mfa"  # this package
]


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