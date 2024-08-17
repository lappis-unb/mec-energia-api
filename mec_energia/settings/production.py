# flake8: noqa
# pylint: skip-file

import environ

from .common import *

env = environ.Env()
prod_env_file = BASE_DIR / ".envs" / ".env.prod"
env.read_env(prod_env_file)


SITE_NAME = "MEPA - Monitoramento de Energia em Plataforma Aberta"
ADMIN_URL = env("DJANGO_ADMIN_URL", default="management/")
DOMAIN = env("DOMAIN_NAME")

DEBUG = env.bool("DJANGO_DEBUG", False)
SECRET_KEY = env("DJANGO_SECRET")

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS = env.list("DJANGO_CSRF_TRUSTED_ORIGINS")


CORS_ALLOWED_ORIGINS = [
    "https://seu-frontend.exemplo.com",  # Seu frontend React
]

# Define quais origens você confia para ignorar verificações CSRF ao postar dados
CSRF_TRUSTED_ORIGINS = [
    "https://seu-frontend.exemplo.com",
]


CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

CORS_ALLOW_HEADERS = [
    "content-disposition",
    "accept-encoding",
    "content-type",
    "accept",
    "origin",
    "authorization",
]


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

DATABASES["default"]["ATOMIC_REQUESTS"] = True
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=100)


# STORAGE STATIC FILES
# ------------------------------------------------------------------------------------------------
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# MEC ENERGIA
# ------------------------------------------------------------------------------------------------
MEC_ENERGIA_URL = env("MEC_ENERGIA_URL")

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
RESET_PASSWORD_TOKEN_TIMEOUT = int(env("RESET_PASSWORD_TOKEN_TIMEOUT"))
RESEND_EMAIL_RESET_PASSWORD_TIMEOUT = int(env("RESEND_EMAIL_RESET_PASSWORD_TIMEOUT"))
MEC_ENERGIA_PASSWORD_ENDPOINT_FIRST_ACCESS = "definir-senha"
MEC_ENERGIA_PASSWORD_ENDPOINT_ADMIN_RESET = "redefinir-senha"
MEC_ENERGIA_PASSWORD_ENDPOINT_USER_RESET = "definir-senha"


# SECURE CONFIGURATION
# -----------------------------------------------------------------------------s
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_HSTS_SECONDS = 518400
# SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True)
# SECURE_CONTENT_TYPE_NOSNIFF = env.bool("DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True)
