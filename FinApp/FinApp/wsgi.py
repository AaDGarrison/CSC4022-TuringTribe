"""
wsgi.py
WSGI config for FinApp project.

Exposes the WSGI callable as a module-level variable named ``application``.
"""

# ----------------------------------------------------------------------------
# Imports

import os

# ----------------------------------------------------------------------------
# Django Imports

from django.core.wsgi import get_wsgi_application

# ----------------------------------------------------------------------------
# Setting Application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FinApp.settings')
application = get_wsgi_application()
