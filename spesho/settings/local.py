from .base import *

# Override default/base.py setting
DEBUG = config('LOCAL_ENV_BOOL')
ALLOWED_HOST = config('LOCAL_ALLOWED_HOSTS')