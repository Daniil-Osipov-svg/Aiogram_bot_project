from .user_handlers import router as user_router
from .dish_handlers import router as dish_router

__all__ = [
    'user_router',
    'dish_router',
]