from .base import *


# Override default/base.py setting
DEBUG = config('DEV_ENV_BOOL')
ALLOWED_HOST = config('DEV_ALLOWED_HOSTS')