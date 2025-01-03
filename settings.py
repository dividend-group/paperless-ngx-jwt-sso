from django.conf import settings

# Ensure custom settings can be read from paperless.conf
PAPERLESS_SSO_JWT_SECRET_KEY = getattr(
    settings, "PAPERLESS_SSO_JWT_SECRET_KEY", "your-default-secret-key"
)
PAPERLESS_SSO_JWT_ALGORITHM = getattr(settings, "PAPERLESS_SSO_JWT_ALGORITHM", "HS256")
