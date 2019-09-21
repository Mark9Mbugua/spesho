from .base import *

# Override default/base.py setting
DEBUG = config('PROD_ENV_BOOL')
ALLOWED_HOST = config('PROD_ALLOWED_HOSTS')