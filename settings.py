import os
from django.conf import settings
from dotenv import load_dotenv

# Tap paperless.conf if it's available
configuration_path = os.getenv("PAPERLESS_CONFIGURATION_PATH")
if configuration_path and os.path.exists(configuration_path):
    load_dotenv(configuration_path)
elif os.path.exists("../paperless.conf"):
    print('...configuration file is here')
    load_dotenv("../paperless.conf")
elif os.path.exists("/etc/paperless.conf"):
    load_dotenv("/etc/paperless.conf")
elif os.path.exists("/usr/local/etc/paperless.conf"):
    load_dotenv("/usr/local/etc/paperless.conf")
# Ensure custom settings can be read from paperless.conf
PAPERLESS_SSO_JWT_SECRET_KEY = getattr(
    settings, "PAPERLESS_SSO_JWT_SECRET_KEY", "your-default-secret-key"
)
PAPERLESS_SSO_JWT_ALGORITHM = getattr(settings, "PAPERLESS_SSO_JWT_ALGORITHM", "HS256")
