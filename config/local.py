from .settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

INTERNAL_IPS = ['127.0.0.1']

INSTALLED_APPS += ['debug_toolbar',] 
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware',]