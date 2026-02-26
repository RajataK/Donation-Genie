from .base import *  # noqa: F401, F403
from .base import BASE_DIR, env

environ = env  # already initialized in base.py
env.read_env(str(BASE_DIR / ".env"), overwrite=False)

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
