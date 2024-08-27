# flake8: noqa
# pylint: skip-file

import environ

from .common import *


env = environ.Env()
ENV_FILE = BASE_DIR / ".envs" / ".env.prod"
env.read_env(ENV_FILE)

SITE_NAME = "MEPA - Monitoramento de Energia em Plataforma Aberta"
ADMIN_URL = env("DJANGO_ADMIN_URL", default="management/")

ENVIRONMENT = env("ENVIRONMENT")
SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env.bool("DJANGO_DEBUG", False)

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS = env.list("DJANGO_CSRF_TRUSTED_ORIGINS")
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOWED_ORIGINS = env.list("DJANGO_CORS_ALLOWED_ORIGINS")

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

DATABASES["default"]["ATOMIC_REQUESTS"] = env.bool("POSTGRES_ATOMIC_REQUESTS", default=False)
DATABASES["default"]["CONN_MAX_AGE"] = env.int("POSTGRES_CONN_MAX_AGE", default=300)


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


# SECURE CONFIGURATION
# -----------------------------------------------------------------------------------------------------
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)  # Redireciona todas as requisições HTTP para HTTPS
# SESSION_COOKIE_SECURE = True  # O cookie de sessão só é enviado em requisições HTTPS
# CSRF_COOKIE_SECURE = True  # O cookie CSRF só é enviado em requisições HTTPS
# SECURE_HSTS_SECONDS = 518400
# SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True)
# SECURE_CONTENT_TYPE_NOSNIFF = env.bool("DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True)
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_HSTS_PRELOAD = True

# -----------------------------------------------------------------------------------------------------
