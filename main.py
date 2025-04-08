import asyncio
import logging
# Импортируем файлы проекта
from dicts import *
from config import *
from handlers import user_handlers, dish_handlers

# Импортируем библиотеки
from aiogram import F #noqa
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, ChatMemberUpdatedFilter, KICKED #noqa

logger = logging.getLogger(__name__)

async def main() -> None:
    # Настройка логирования
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s'
               '[%(asctime)s] - %(name)s - %(message)s')

    # Получаем токен из конфигурационного файла
    config: Config = load_config()

    bot = Bot(token=config.bot.token)
    dp = Dispatcher()

    # Регистрация всех обработчиков
    dp.include_router(user_handlers.router)
    dp.include_router(dish_handlers.router)

    # Запуск бота
    if __name__ == '__main__':
        logging.info('Бот запущен!')
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)

asyncio.run(main())