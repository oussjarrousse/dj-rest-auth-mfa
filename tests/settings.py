import os
from django.conf.global_settings import PASSWORD_HASHERS as DEFAULT_PASSWORD_HASHERS

SECRET_KEY = "fake-key-for-testing"
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",    
    # TODO: Add these to documentation 
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "mfa",
    "allauth",    
    "dj_rest_auth",
    "dj_rest_auth_mfa",
]

ROOT_URLCONF="dj_rest_auth_mfa.urls"


MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # TODO: Add these to documentation
    "allauth.account.middleware.AccountMiddleware",
]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

# ADD TO DOCUMENTATIONS

MFA_UNALLOWED_METHODS = (
    "U2F",
    "FIDO",
    "FIDO2",
    "Email",
    "Trusted_Devices",
)  # Methods that shouldn't be allowed for the user e.g ('TOTP','U2F',)
MFA_LOGIN_CALLBACK = (
    ""  # A function that should be called by username to login the user in session
)
MFA_RECHECK = True  # Allow random rechecking of the user
MFA_REDIRECT_AFTER_REGISTRATION = (
    "home"  # Allows Changing the page after successful registeration
)
MFA_SUCCESS_REGISTRATION_MSG = "Go to Security Home"  # The text of the link
MFA_RECHECK_MIN = 10  # Minimum interval in seconds
MFA_RECHECK_MAX = 30  # Maximum in seconds
MFA_QUICKLOGIN = True  # Allow quick login for returning users by provide only their 2FA
MFA_ALWAYS_GO_TO_LAST_METHOD = False  # Always redirect the user to the last method used to save a click (Added in 2.6.0).
MFA_RENAME_METHODS = (
    {}
)  # Rename the methods in a more user-friendly way e.g {"RECOVERY":"Backup Codes"} (Added in 2.6.0)
MFA_HIDE_DISABLE = ("FIDO2",)  # Can the user disable his key (Added in 1.2.0).
MFA_OWNED_BY_ENTERPRISE = False  # Who owns security keys
MFA_ENFORCE_RECOVERY_METHOD = True  # 
PASSWORD_HASHERS = DEFAULT_PASSWORD_HASHERS  # Comment if PASSWORD_HASHER already set in your settings.py
PASSWORD_HASHERS += ["mfa.recovery.Hash"]
RECOVERY_ITERATION = 720000  # Number of iteration for recovery code, higher is more secure, but uses more resources for generation and check...
# ON TOP OF DJANGO MFA2
MFA_MANDATORY = False
MFA_ADAPTER_CLASS = "dj_rest_auth_mfa.adapters.DjangoMFA2Adapter"
MFA_GRACE_WINDOW_DAYS = 7
TOKEN_ISSUER_NAME="dj-rest-auth-mfa"      #TOTP Issuer name

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"