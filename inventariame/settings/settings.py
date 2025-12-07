import os

env = os.getenv("DJANGO_ENV", "dev")

if env == "prod":
    from .production import *
else:
    from .development import *
