import jwt
from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import os

class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        """
        Authenticate the user using JWT passed via GET query parameters.
        """
        token = request.GET.get("jwt")
        if not token:
            return None  # No JWT token provided

        try:
            # Decode the JWT using the secret key and algorithm
            secret_key = os.getenv("PAPERLESS_SSO_JWT_SECRET_KEY")
            algorithm = os.getenv("PAPERLESS_SSO_JWT_ALGORITHM", "HS256")
            payload = jwt.decode(token, secret_key, algorithms=[algorithm])

            # Validate payload content (ensure "username" exists, for example)
            username = payload.get("username")
            if not username:
                raise AuthenticationFailed("Invalid JWT payload: 'username' missing")

            # Retrieve or create a user
            user, _ = User.objects.get_or_create(username=username)
            return (user, token)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("JWT token has expired")
        except jwt.InvalidTokenError as e:
            raise AuthenticationFailed(f"Invalid JWT token: {str(e)}")
