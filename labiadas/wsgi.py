"""
WSGI config for labiadas project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os, locale

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "labiadas.settings")


# locale.setlocale(locale.LC_ALL, 'en_CA.utf-8')

application = get_wsgi_application()
