from .base import *

# Override default/base.py setting
DEBUG = config('STAGE_ENV_BOOL')
ALLOWED_HOST = config('STAGE_ALLOWED_HOSTS')