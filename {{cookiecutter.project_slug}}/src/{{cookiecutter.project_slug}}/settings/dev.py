from .base import *

# Django Debug Toolbar
# insert before third last element value
INSTALLED_APPS.insert(
    -3, 'debug_toolbar',    # https://github.com/jazzband/django-debug-toolbar
)

# Additional middleware introduced by debug toolbar
# insert after first element value
MIDDLEWARE.insert(
    1, 'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ALLOWED_HOSTS = []
INTERNAL_IPS = ['127.0.0.1', '::1']

# Example for Gmail
"""
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
which_username = os.environ['SOME_USERID']
which_domain = '@gmail.com'
EMAIL_HOST_USER = which_username + which_domain
EMAIL_HOST_PASSWORD = os.environ['SOME_USERAUTH']
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
"""

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# BASE_URL required for notification emails
BASE_URL = 'http://localhost:8000'
