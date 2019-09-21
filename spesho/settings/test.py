from .base import *


# Override default/base.py setting
DEBUG = config('TEST_ENV_BOOL')
ALLOWED_HOST = config('TEST_ALLOWED_HOSTS')