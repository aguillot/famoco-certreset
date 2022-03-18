from config.settings.dev import SECRET_KEY
from .base import *

SECRET_KEY = get_env_variable("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["famoco-certreset.herokuapp.com"]
