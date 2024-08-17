import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

DEBUG = os.getenv("ENVIRONMENT") != "production"
TEST = os.getenv("ENVIRONMENT") == "test"

ALLOWED_HOSTS = ["*"]

ENVIRONMENT = os.getenv("ENVIRONMENT")


# Parâmetros de recomendação de contrato
MINIMUM_ENERGY_BILLS_FOR_RECOMMENDATION = 6
IDEAL_ENERGY_BILLS_FOR_RECOMMENDATION = 12
MINIMUM_PERCENTAGE_DIFFERENCE_FOR_CONTRACT_RENOVATION = 0.05
RECOMMENDATION_METHOD = os.getenv("RECOMMENDATION_METHOD")

# Valor de demanda mínimo na nova resolução
NEW_RESOLUTION_MINIMUM_DEMAND = 30

# Configurações do servidor SMTP
SMTP_EMAIL_SERVER = os.getenv("SMTP_EMAIL_SERVER")
SMTP_EMAIL_PORT = os.getenv("SMTP_EMAIL_PORT")
SMTP_EMAIL_USER = os.getenv("SMTP_EMAIL_USER")
SMTP_EMAIL_PASSWORD = os.getenv("SMTP_EMAIL_PASSWORD")

# Password reset
RESET_PASSWORD_TOKEN_TIMEOUT = int(os.getenv("RESET_PASSWORD_TOKEN_TIMEOUT"))
RESEND_EMAIL_RESET_PASSWORD_TIMEOUT = int(os.getenv("RESEND_EMAIL_RESET_PASSWORD_TIMEOUT"))
MEC_ENERGIA_PASSWORD_ENDPOINT_FIRST_ACCESS = "definir-senha"
MEC_ENERGIA_PASSWORD_ENDPOINT_ADMIN_RESET = "redefinir-senha"
MEC_ENERGIA_PASSWORD_ENDPOINT_USER_RESET = "definir-senha"
# -----------------------------------------------------------------

# MEDIA_ROOT  parametros para configuração de salvamento da pasta media

MEDIA_ROOT = "./media"

# -----------------------------------------------------------------

INSTALLED_APPS = [
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


# MIDDLEWARE
# ------------------------------------------------------------------------------------------------
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

CORS_ORIGIN_WHITELIST = ("http://localhost:3000",)

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

CORS_ALLOW_HEADERS = ["content-disposition", "accept-encoding", "content-type", "accept", "origin", "authorization"]


# GENERAL
# ------------------------------------------------------------------------------------------------
ROOT_URLCONF = "mec_energia.urls"
WSGI_APPLICATION = "mec_energia.wsgi.application"
AUTH_USER_MODEL = "users.CustomUser"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

APPEND_SLASH = True
LOGIN_REDIRECT_URL = "/"


# TEMPLATES
# ------------------------------------------------------------------------------------------------
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


# DATABASES
# ------------------------------------------------------------------------------------------------
if TEST:
    DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "HOST": env("POSTGRES_HOST"),
            "PORT": env("POSTGRES_PORT"),
            "NAME": env("POSTGRES_DB"),
            "USER": env("POSTGRES_USER"),
            "PASSWORD": env("POSTGRES_PASSWORD"),
        }
    }


# PASSWORD VALIDATORS
# ------------------------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# INTERNATIONALIZATION
# ------------------------------------------------------------------------------------------------
TIME_ZONE = "America/Sao_Paulo"
LANGUAGE_CODE = "en-us"

USE_I18N = True
USE_L10N = True
USE_TZ = False


# STATIC FILES & MEDIA FILES (CSS, JavaScript, Images)
# ------------------------------------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_ROOT.mkdir(parents=True, exist_ok=True)

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "mediafiles"
MEDIA_ROOT.mkdir(parents=True, exist_ok=True)


STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

if os.getenv("ENVIRONMENT") != "production":
    PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]


# DJANGO REST FRAMEWORK
# ------------------------------------------------------------------------------------------------
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

if TEST:
    del REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"]
    del REST_FRAMEWORK["DEFAULT_PARSER_CLASSES"]
    SOUTH_TESTS_MIGRATE = False


# MEC ENERGIA
# ------------------------------------------------------------------------------------------------
MEC_ENERGIA_URL = os.getenv("MEC_ENERGIA_URL")

# Parâmetros de recomendação de contrato
MINIMUM_ENERGY_BILLS_FOR_RECOMMENDATION = 6
IDEAL_ENERGY_BILLS_FOR_RECOMMENDATION = 12
MINIMUM_PERCENTAGE_DIFFERENCE_FOR_CONTRACT_RENOVATION = 0.05
RECOMMENDATION_METHOD = os.getenv("RECOMMENDATION_METHOD")

# Valor de demanda mínimo na nova resolução
NEW_RESOLUTION_MINIMUM_DEMAND = 30

# Email
MEC_ENERGIA_EMAIL = os.getenv("MEC_ENERGIA_EMAIL")
MEC_ENERGIA_EMAIL_APP_PASSWORD = os.getenv("MEC_ENERGIA_EMAIL_APP_PASSWORD")

# Password reset
RESET_PASSWORD_TOKEN_TIMEOUT = int(os.getenv("RESET_PASSWORD_TOKEN_TIMEOUT"))
RESEND_EMAIL_RESET_PASSWORD_TIMEOUT = int(os.getenv("RESEND_EMAIL_RESET_PASSWORD_TIMEOUT"))
MEC_ENERGIA_PASSWORD_ENDPOINT_FIRST_ACCESS = "definir-senha"
MEC_ENERGIA_PASSWORD_ENDPOINT_ADMIN_RESET = "redefinir-senha"
MEC_ENERGIA_PASSWORD_ENDPOINT_USER_RESET = "definir-senha"
