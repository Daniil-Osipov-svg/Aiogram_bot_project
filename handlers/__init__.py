from .user_handlers import router as user_router
from .dish_handlers import router as dish_router
from .callback_handlers import router as callback_router

__all__ = [
    'user_router',
    'dish_router',
    'callback_router'
]