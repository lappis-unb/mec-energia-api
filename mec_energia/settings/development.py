# flake8: noqa
# pylint: skip-file

import environ

from .common import *


env = environ.Env()
ENV_FILE = BASE_DIR / ".envs" / ".env.dev"
env.read_env(ENV_FILE)

ENVIRONMENT = env("ENVIRONMENT")
SECRET_KEY = "django-insecure-#123!@#$%^&*()_+"
DEBUG = True

ALLOWED_HOSTS = ["mepa-api", "localhost", "127.0.0.1", "0.0.0.0", "[::1]"]
CSRF_TRUSTED_ORIGINS = ["http://mepa-web:3000", "http://localhost:3000"]
CORS_ALLOW_ALL_ORIGINS = True


# DATABASES
# ------------------------------------------------------------------------------------------------
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


# MEC ENERGIA
# ------------------------------------------------------------------------------------------------
MEC_ENERGIA_URL = env("FRONT_SERVICE_URL")

# Parâmetros de recomendação de contrato
MINIMUM_ENERGY_BILLS_FOR_RECOMMENDATION = 6
IDEAL_ENERGY_BILLS_FOR_RECOMMENDATION = 12
MINIMUM_PERCENTAGE_DIFFERENCE_FOR_CONTRACT_RENOVATION = 0.05
RECOMMENDATION_METHOD = env("RECOMMENDATION_METHOD")

# Valor de demanda mínimo na nova resolução
NEW_RESOLUTION_MINIMUM_DEMAND = 30

# Email
MEC_ENERGIA_EMAIL = env("FRONT_URL")
MEC_ENERGIA_EMAIL_APP_PASSWORD = env("MEC_ENERGIA_EMAIL_APP_PASSWORD")

# Password reset
RESET_PASSWORD_TOKEN_TIMEOUT = env.int("RESET_PASSWORD_TOKEN_TIMEOUT")
RESEND_EMAIL_RESET_PASSWORD_TIMEOUT = env.int("RESEND_EMAIL_RESET_PASSWORD_TIMEOUT")
MEC_ENERGIA_PASSWORD_ENDPOINT_FIRST_ACCESS = "definir-senha"
MEC_ENERGIA_PASSWORD_ENDPOINT_ADMIN_RESET = "redefinir-senha"
MEC_ENERGIA_PASSWORD_ENDPOINT_USER_RESET = "definir-senha"


# DEBUG TOOLBAR
# ------------------------------------------------------------------------------------------------
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
INSTALLED_APPS += ["debug_toolbar"]
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: True,
    "INTERCEPT_REDIRECTS": False,
    "ALLOWED_HOSTS": ["*"],
}


# DJANGO EXTENSIONS
# ------------------------------------------------------------------------------------------------
INSTALLED_APPS += ["django_extensions"]


# SECURITY DISABLED FOR DEVELOPMENT
# ------------------------------------------------------------------------------------------------
SECURE_BROWSER_XSS_FILTER = False
SECURE_CONTENT_TYPE_NOSNIFF = False
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False


# ENVIRONMENT TEST
# ------------------------------------------------------------------------------------------------
if ENVIRONMENT == "test":
    del REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"]
    del REST_FRAMEWORK["DEFAULT_PARSER_CLASSES"]
    SOUTH_TESTS_MIGRATE = False

    PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
