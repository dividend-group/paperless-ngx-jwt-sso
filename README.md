### **README.md**

# **Custom JWT SSO Integration for Paperless-ngx**

This package provides a custom JWT-based Single Sign-On (SSO) solution for Paperless-ngx, allowing users to authenticate directly using JWT tokens via a URL.

---

## **Features**
- Seamless integration with Paperless-ngx using `paperless.conf` for configuration.
- Secure JWT validation with support for custom secrets and algorithms.
- Middleware implementation to authenticate users dynamically.
- Easy setup without modifying Paperless-ngx source code.

---

## **Prerequisites**
- Python installed in the Paperless-ngx environment.
- Paperless-ngx installed and configured.
- A JWT generator in your external application that matches the secret and algorithm used in Paperless-ngx.

---

## **Installation Steps**

### **1. Configuration**

Add the following parameters to your `paperless.conf` file:

```bash
# Enable custom SSO authentication
PAPERLESS_SSO_ENABLED=true

# JWT Secret Key and Algorithm
PAPERLESS_SSO_JWT_SECRET_KEY=your-secret-key-here
PAPERLESS_SSO_JWT_ALGORITHM=HS256  # Adjust as needed
```

### **2. Install the `jwt_sso` Package**

From the Paperless root directory:

1. Navigate to the `src` directory:

   ```bash
   cd src
   ```

2. Create a directory for the package and clone the repository:

   ```bash
   mkdir jwt_sso
   cd jwt_sso
   git clone <repository-url> .
   ```

---

### **3. Update `settings.py`**

Navigate to the `paperless/src/paperless` directory and open the `settings.py` file.

1. **Add Custom Module Path**  
   Add this snippet at the top of the file:

   ```python
   import os
   import sys

   ###################################################################
   # Adding the current directory to Python path for custom modules
   current_dir = os.path.dirname(os.path.abspath(__file__))
   parent_dir = os.path.dirname(current_dir)  # Go one step back

   sys.path.append(parent_dir)
   ###################################################################
   ```

2. **Add JWT SSO Settings**  
   Add these lines to define JWT SSO settings:

   ```python
   # JWT SSO Authentication settings
   PAPERLESS_SSO_JWT_SECRET_KEY = os.getenv("PAPERLESS_SSO_JWT_SECRET_KEY", "default_secret_key")
   PAPERLESS_SSO_JWT_ALGORITHM = os.getenv("PAPERLESS_SSO_JWT_ALGORITHM", "HS256")
   ```

3. **Enable Custom Middleware Dynamically**  
   Add this snippet after the `MIDDLEWARE` variable declaration to include the JWT middleware:

   ```python
   ###################################################################
   # JWT Custom Authentication Middleware
   if os.getenv("PAPERLESS_SSO_ENABLED", "False").lower() == "true":
       try:
           # Ensure AuthenticationMiddleware is present
           auth_middleware_index = MIDDLEWARE.index("django.contrib.auth.middleware.AuthenticationMiddleware")
           # Insert JWTAuthMiddleware directly after AuthenticationMiddleware
           MIDDLEWARE.insert(auth_middleware_index + 1, "jwt_sso.middleware.JWTAuthMiddleware")
       except ValueError:
           # If AuthenticationMiddleware is missing, raise an error
           raise RuntimeError(
               "AuthenticationMiddleware is not in MIDDLEWARE. "
               "Please add it before enabling PAPERLESS_SSO."
           )
   ###################################################################
   ```

---

### **4. Generate JWT Tokens**

Ensure that the JWT tokens are generated with the following criteria:
- **Matching Secret Key and Algorithm:**  
  Use the same `PAPERLESS_SSO_JWT_SECRET_KEY` and `PAPERLESS_SSO_JWT_ALGORITHM` values as configured in Paperless-ngx.
- **Payload Requirements:**  
  The payload must include a `username` field.

Example JWT payload:

```json
{
  "username": "john_doe"
}
```

---

### **5. Authenticate Using JWT**

To authenticate, append the JWT token to the base URL as follows:

```text
http://localhost:8000?jwt=YOUR_JWT_TOKEN
```

- If the token is valid, the user will be logged in and redirected to the homepage.
- If the token is invalid or missing, the user will be redirected to the login page (`/accounts/login/`).

---

## **Troubleshooting**

- **Middleware Order Issue:**  
  Ensure the `JWTAuthMiddleware` follows `AuthenticationMiddleware` in the middleware stack.
- **Invalid JWT Token:**  
  Verify that the secret key and algorithm match between the JWT generator and Paperless-ngx.
- **Module Discovery Error:**  
  Confirm that the `jwt_sso` package is correctly installed and that the parent directory is added to `sys.path` in `settings.py`.

---

## **License**
This project is open-source. Feel free to contribute and modify as needed.

--- 

Enjoy secure and seamless authentication with your custom JWT SSO integration!