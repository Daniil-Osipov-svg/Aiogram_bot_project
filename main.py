# Импортируем файлы проекта
from dicts import *
from config import *
from handlers import register_all_handlers

# Импортируем библиотеки
from aiogram import F #noqa
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, ChatMemberUpdatedFilter, KICKED #noqa
from aiogram.types import Message, ChatMemberUpdated #noqa

# Получаем токен из конфигурационного файла
config = load_config()

bot = Bot(token=config.bot.token)
dp = Dispatcher()

# Регистрация всех обработчиков
register_all_handlers(dp)

# Запуск бота
if __name__ == '__main__':
    print('Бот запущен!')
    dp.run_polling(bot)