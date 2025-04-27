import asyncio
import logging
# Импортируем файлы проекта
from config import *
from handlers import user_handlers, dish_handlers, callback_handlers, tdee_handlers
from database.models import async_main


# Импортируем библиотеки
from aiogram import Bot, Dispatcher

# Редис
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

redis = Redis(host='localhost')
storage = RedisStorage(redis=redis)


logger = logging.getLogger(__name__)

async def main():

    # Привязываем функции к событиям
    await async_main()
    # Настройка логирования
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s'
               '[%(asctime)s] - %(name)s - %(message)s')

    # Получаем токен из конфигурационного файла
    config = load_config()

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