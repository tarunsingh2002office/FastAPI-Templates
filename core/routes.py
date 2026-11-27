from fastapi import APIRouter
from users.userRoutes import user_router
api_router = APIRouter()

# Include all feature routers
api_router.include_router(user_router)
