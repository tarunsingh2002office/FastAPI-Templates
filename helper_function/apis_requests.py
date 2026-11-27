from fastapi import Header

# Add `token: str = Depends(get_current_user)` to any protected view.
# The real check is done by middleware/AuthMiddleware.py - this dependency only
# makes Swagger (/docs) show a `token` header input so you can test the route.
async def get_current_user(token: str = Header(..., description="User authentication token")):
    return token
