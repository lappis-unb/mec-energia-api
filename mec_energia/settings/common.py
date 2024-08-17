from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent

DEBUG = True
ALLOWED_HOSTS = []


# APPS
# ------------------------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
]

EXTERNAL_APPS = [
    "corsheaders",
    "drf_yasg",
    "rest_framework",
    "rest_framework.authtoken",
]

LOCAL_APPS = [
    "contracts",
    "global_search_recommendation",
    "recommendation",
    "tariffs",
    "users",
    "universities",
]

INSTALLED_APPS = DJANGO_APPS + EXTERNAL_APPS + LOCAL_APPS


# TEMPLATES
# ---------------------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# MIDDLEWARE
# ---------------------------------------------------------------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# GENERAL
# ---------------------------------------------------------------------------------------
ROOT_URLCONF = "mec_energia.urls"
WSGI_APPLICATION = "mec_energia.wsgi.application"
AUTH_USER_MODEL = "users.CustomUser"

APPEND_SLASH = True
LOGIN_REDIRECT_URL = "/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# PASSWORD VALIDATORS
# ---------------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# INTERNATIONALIZATION
# ---------------------------------------------------------------------------------------
TIME_ZONE = "America/Sao_Paulo"
LANGUAGE_CODE = "en-us"

USE_I18N = True
USE_L10N = True
USE_TZ = False


# STATIC FILES & MEDIA FILES (CSS, JavaScript, Images)
# ---------------------------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_ROOT.mkdir(parents=True, exist_ok=True)

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "mediafiles"
MEDIA_ROOT.mkdir(parents=True, exist_ok=True)


# DJANGO REST FRAMEWORK
# ---------------------------------------------------------------------------------------
REST_FRAMEWORK = {
    "COERCE_DECIMAL_TO_STRING": False,
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_RENDERER_CLASSES": (
        "djangorestframework_camel_case.render.CamelCaseJSONRenderer",
        "djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer",
    ),
    "DEFAULT_PARSER_CLASSES": (
        "djangorestframework_camel_case.parser.CamelCaseFormParser",
        "djangorestframework_camel_case.parser.CamelCaseMultiPartParser",
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
    ),
}
