from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
import logging
import jwt
from django.conf import settings

logger = logging.getLogger(__name__)

class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Ensure the JWT token is present in the URL
        jwt_token = request.GET.get("jwt")
        if jwt_token:
            try:
                # Decode the JWT token and get the username 
                payload = jwt.decode(
                    jwt_token,
                    settings.PAPERLESS_SSO_JWT_SECRET_KEY,
                    algorithms=[settings.PAPERLESS_SSO_JWT_ALGORITHM]
                )
                username = payload.get("username")
                if not username:
                    logger.error("JWT payload is missing the 'username' field.")
                    raise ValueError("Invalid JWT payload")

                # Retrieve or create the user
                user, created = User.objects.get_or_create(username=username)
                if created:
                    logger.info(f"Created a new user '{username}'.")

                # Log the user in, specifying the backend
                user.backend = "django.contrib.auth.backends.ModelBackend"
                login(request, user, backend=user.backend)
                logger.info(f"Authenticated user '{username}' via JWT.")
                return redirect("/")  # Redirect to homepage

            except jwt.ExpiredSignatureError:
                logger.error("JWT token has expired.")
            except jwt.InvalidTokenError:
                logger.error("Invalid JWT token.")
            except Exception as e:
                logger.error(f"Error authenticating user via JWT: {e}")
                return redirect("/accounts/login/")  # Redirect to login on failure

        # Continue processing the request
        response = self.get_response(request)
        return response