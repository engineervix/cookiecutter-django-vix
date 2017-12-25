import os
import random
import string

from .base import *

# add your production settings here

# INSTALLED_APPS.append('maintenancemode')
INSTALLED_APPS.insert(
    -5, 'captcha',                              # https://github.com/praekelt/django-recaptcha
    len(INSTALLED_APPS), 'maintenancemode',     # https://github.com/alsoicode/django-maintenancemode-2
)

# MIDDLEWARE.append('maintenancemode.middleware.MaintenanceModeMiddleware')
MIDDLEWARE.insert(
    len(MIDDLEWARE), 'maintenancemode.middleware.MaintenanceModeMiddleware',
)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

{% if cookiecutter.use_sparkpost == 'y' %}
SPARKPOST_API_KEY = os.environ['SPARKPOST_USERAUTH']

EMAIL_BACKEND = 'sparkpost.django.email_backend.SparkPostEmailBackend'
{% endif %}

"""
SPARKPOST_OPTIONS = {
    'track_opens': False,
    'track_clicks': False,
    'transactional': True,
}
"""

LIST_OF_EMAIL_RECIPIENTS += [
    'add',
    'more',
    'email',
    'addresses',
    'here',
    'if',
    'required'
]

DEFAULT_FROM_EMAIL = "Do Not Reply <do_not_reply@{{cookiecutter.domain_name}}>"

RECAPTCHA_PUBLIC_KEY = os.environ['RECAPTCHA_SITE_KEY']
RECAPTCHA_PRIVATE_KEY = os.environ['RECAPTCHA_PRIVATE_KEY']

# include nocaptcha recaptcha setting
NOCAPTCHA = True

# To make reCAPTCHA work in ajax-loaded forms:
# CAPTCHA_AJAX = True

# enable SSL flag, if the data exchange needs to be secure. Not needed for small apps
RECAPTCHA_USE_SSL = True

MAINTENANCE_503_TEMPLATE = 'maintenance_mode/503.html'
