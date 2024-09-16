"""
WSGI config for mec_energia project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

environment = os.environ.get("ENVIRONMENT", "production")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"mec_energia.settings.{environment}")

application = get_wsgi_application()
