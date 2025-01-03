import jwt
from django.contrib.auth import login
from django.shortcuts import redirect
from django.utils.timezone import now
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.GET.get("jwt")
        if token:
            logger.info("JWT token detected in the query parameters.")
            try:
                # Decode JWT token
                payload = jwt.decode(
                    token,
                    settings.PAPERLESS_SSO_JWT_SECRET_KEY,
                    algorithms=[settings.PAPERLESS_SSO_JWT_ALGORITHM],
                )
                username = payload.get("username")
                if not username:
                    logger.warning("JWT token missing 'username' field.")
                else:
                    from django.contrib.auth.models import User
                    user, _ = User.objects.get_or_create(username=username)

                    if not user.is_authenticated:
                        # Log the user in
                        login(request, user)
                        logger.info(f"Authenticated user '{username}' via JWT.")
                        return redirect("/")  # Redirect to homepage after login
            except jwt.ExpiredSignatureError:
                logger.error("JWT token has expired.")
            except jwt.InvalidTokenError:
                logger.error("Invalid JWT token.")
        return self.get_response(request)