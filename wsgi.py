"""
WSGI config for mama100 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mama100.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
#####for websocket
from django_websocket.wsgi import get_wsgi_websocket_application
websocket = get_wsgi_websocket_application()