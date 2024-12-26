# Custom JWT SSO Authentication for Paperless-Ngx

This package provides a clean and modular implementation of a Single Sign-On (SSO) authentication system using JWT tokens for Paperless-Ngx. It allows users to authenticate directly into the Paperless-Ngx UI by passing a JWT token via a URL query parameter. The package ensures no modifications are made to the Paperless-Ngx source code by relying on external configuration.

---

## **Features**

- Authenticate directly into Paperless-Ngx UI using JWT tokens.
- Validate tokens internally without external calls.
- Extends Paperless-Ngx using a modular design.
- Configurable via environment variables in `paperless.conf`.

---

## **Installation Guide**

### **1. Prerequisites**
- Python environment with Paperless-Ngx installed as a package.
- Ensure you have access to manage `paperless.conf`.

### **2. Install the Custom Package**
Install the custom SSO package into your Python environment:

```bash
pip install custom-sso-auth
```

### **3. Configure `paperless.conf`**
Add the following environment variables to your `paperless.conf` file:

```env
# Enable custom SSO authentication
PAPERLESS_SSO_ENABLED=True

# JWT Secret Key and Algorithm
PAPERLESS_SSO_JWT_SECRET_KEY=your_sso_secret_key
PAPERLESS_SSO_JWT_ALGORITHM=HS256
```

Replace `your_sso_secret_key` with the secret key used to sign your JWT tokens. The algorithm defaults to `HS256` but can be adjusted as needed.

### **4. Middleware and Authentication Setup**
The custom package includes:
- **Middleware** to parse and handle JWT tokens from the URL.
- **Custom Authentication** to validate tokens and authenticate users.

To activate these features, dynamically override the settings in `paperless.conf`. Ensure your `settings.py` contains the following logic:

```python
import os

if os.getenv("PAPERLESS_SSO_ENABLED", "False").lower() == "true":
    REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"].insert(
        0, "custom_sso_auth.authentication.CustomJWTAuthentication"
    )
    MIDDLEWARE.insert(0, "custom_sso_auth.middleware.JWTAuthMiddleware")
```

This ensures that the custom authentication and middleware are loaded when SSO is enabled.

### **5. Using the SSO System**
To access the Paperless-Ngx UI with JWT authentication, append the token to the URL as a query parameter:

```text
https://your-paperless-domain.com?jwt=your_encoded_jwt_token
```

- The middleware extracts the token from the `jwt` query parameter.
- The authentication system decodes and validates the token.
- If valid, the user is authenticated and logged into the UI.

---

## **How It Works**

### **JWT Token Validation**
The package validates the JWT token using the secret key and algorithm defined in `paperless.conf`. It:
- Decodes the token locally.
- Checks the payload for a `username` field.
- Retrieves or creates the corresponding user in the system.

### **Middleware Workflow**
The middleware intercepts incoming requests, checks for the `jwt` query parameter, and sets the `Authorization` header for internal authentication.

### **Custom Authentication Class**
The authentication class processes the `Authorization` header, validates the token, and authenticates the user if the token is valid.

---

## **Key Benefits**

- **Secure**: All validation is performed internally.
- **Modular**: No changes to Paperless-Ngx source code.
- **Flexible**: Fully configurable via `paperless.conf`.
- **User-Friendly**: Seamless integration for end-users.

---

## **Troubleshooting**

- Ensure `PAPERLESS_SSO_ENABLED` is set to `True` in `paperless.conf`.
- Verify the `PAPERLESS_SSO_JWT_SECRET_KEY` matches the key used to sign your tokens.
- Check server logs for detailed error messages if authentication fails.

---

## **Future Improvements**

- Support for additional authentication methods.
- Enhanced error handling and logging.
- Token revocation and expiration management.

---

For questions or issues, feel free to contact the maintainer or refer to the documentation.
