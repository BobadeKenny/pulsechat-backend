from rest_framework_simplejwt.tokens import AccessToken


class TokenAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, scope, receive, send):
        headers = dict(scope.get("headers", []))
        authorization_header = headers.get(b"authorization")
        if authorization_header:
            auth_value = authorization_header.decode()
            token = auth_value.split()[1]
            try:
                access_token = AccessToken(token)
                scope["user_id"] = access_token["user_id"]
            except Exception:
                scope["user_id"] = None

        return self.get_response(scope, receive, send)
