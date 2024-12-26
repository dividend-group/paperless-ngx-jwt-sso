from django.http import HttpResponseRedirect
import os

class JWTAuthMiddleware:
    """
    Middleware to handle JWT authentication via GET parameters.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if os.getenv("PAPERLESS_SSO_ENABLED", "False").lower() == "true":
            jwt_token = request.GET.get("jwt")
            if jwt_token:
                # Automatically authenticate the user using the token
                request.META["HTTP_AUTHORIZATION"] = f"Bearer {jwt_token}"

        return self.get_response(request)
