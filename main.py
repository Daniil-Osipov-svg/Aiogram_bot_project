from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

#API моего чат бота
BOT_TOKEN = '7774687817:AAGlmbpI-HhrXadQsgu5LyWqNKlsOcEAx9E'


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command(commands=['start']))
async def start_command(message: Message):
    await message.answer('Привет!\nМеня зовут TunWheel!')

# Обработчик команды /help
@dp.message(Command(commands=['help']))
async def help_command(message: Message):
    await message.answer('Я ваш помощник для подсчёта калорий.\n'
                        'Я могу помочь вам с подсчётом калорий и составлением рациона питания.\n'
                        'Напишите /start, чтобы начать!')

#Эхо-бот
@dp.message()
async def echo_message(message: Message) -> None:
    await message.reply(message.text or 'Пустое сообщение!')

# Запуск бота
if __name__ == '__main__':
    print('Бот запущен!')
    dp.run_polling(bot)