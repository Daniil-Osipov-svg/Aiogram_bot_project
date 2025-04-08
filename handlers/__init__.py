from .user_handlers import register_user_handlers
from .dish_handlers import register_dish_handlers

def register_all_handlers(dp):
    """Регистрирует все обработчики сообщений"""
    register_user_handlers(dp)
    register_dish_handlers(dp)