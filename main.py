import asyncio
import logging
# Импортируем файлы проекта
from dicts import *
from config import *
from handlers import user_handlers, dish_handlers, callback_handlers, tdee_handlers

# База данных
#from database.engine import create_db, drop_db

# Импортируем библиотеки
from aiogram import Bot, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
from aiogram.filters import Command, ChatMemberUpdatedFilter, KICKED #noqa

# Редис
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

redis = Redis(host='localhost')
storage = RedisStorage(redis=redis)


logger = logging.getLogger(__name__)

async def on_startup(bot):
    # Создаем базу данных, если она не существует
    #await create_db()
    logger.info("База данных создана")

async def on_shutdown(bot):
    # Закрываем соединение с базой данных
    logger.info("Бот завершает работу")

async def main():

    # Привязываем функции к событиям
    #dp.register_startup(on_startup)
    #dp.register_shutdown(on_shutdown)

    # Настройка логирования
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s'
               '[%(asctime)s] - %(name)s - %(message)s')

    # Получаем токен из конфигурационного файла
    config: Config = load_config()

    bot = Bot(token=config.bot.token)
    dp = Dispatcher(storage=storage)

    # Регистрация всех обработчиков
    dp.include_router(user_handlers.router)
    dp.include_router(dish_handlers.router)
    dp.include_router(callback_handlers.router)
    dp.include_router(tdee_handlers.router)

    # Запуск бота
    if __name__ == '__main__':
        logging.info('Бот запущен!')
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)

asyncio.run(main())