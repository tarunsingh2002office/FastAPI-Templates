import jwt
from starlette.types import ASGIApp, Scope, Receive, Send
from starlette.responses import JSONResponse
from core.config import jwt_settings

EXCLUDED_PATHS = {
    "/check", "/docs", "/redoc", "/openapi.json",
    "/user/createUser",
}
OPTIONAL_TOKEN_PATHS = set()
# Paths that end in an id. No token = guest (the view decides what a guest
# gets). A WRONG or EXPIRED token is still a 401.
OPTIONAL_TOKEN_PREFIXES = ()


class AuthMiddleware:
    """Pure ASGI middleware. Faster than BaseHTTPMiddleware.
    Decodes JWT once, sets userId in scope['state']. No DB hit."""

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        # Skip non-HTTP (WebSocket, lifespan)
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        method = scope["method"]
        path = scope["path"]

        # Skip CORS preflight and excluded paths
        if (method == "OPTIONS"
            or path in EXCLUDED_PATHS):
            await self.app(scope, receive, send)
            return

        # Extract token from headers (headers are list of (bytes, bytes) tuples in ASGI)
        token = None
        for name, value in scope["headers"]:
            if name == b"token":
                token = value.decode("latin-1")
                break

        if not token:
            if path in OPTIONAL_TOKEN_PATHS or path.startswith(OPTIONAL_TOKEN_PREFIXES):
                await self.app(scope, receive, send)
                return
            resp = JSONResponse({"msg": "token not present"}, status_code=401)
            await resp(scope, receive, send)
            return

        try:
            decoded = jwt.decode(token, jwt_settings.SUGAR_VALUE, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            resp = JSONResponse({"msg": "Token has expired"}, status_code=401)
            await resp(scope, receive, send)
            return
        except jwt.InvalidTokenError:
            resp = JSONResponse({"msg": "Invalid token"}, status_code=401)
            await resp(scope, receive, send)
            return

        # Set state on scope so downstream can read request.state.userId
        if "state" not in scope:
            scope["state"] = {}
        scope["state"]["userId"] = decoded.get("id")

        await self.app(scope, receive, send)
