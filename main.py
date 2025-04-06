from aiogram import F #noqa
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, ChatMemberUpdatedFilter, KICKED #noqa
from aiogram.types import Message, ChatMemberUpdated #noqa

#API моего чат бота
BOT_TOKEN = '7774687817:AAGlmbpI-HhrXadQsgu5LyWqNKlsOcEAx9E'


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Пользователи
users = {}

# Обработчик команды /start
async def start_command(message: Message):
    # Проверяем, есть ли пользователь в списке
    # Если нет, добавляем его

    # Убираем срабатывание ошибки mypy
    if message.from_user is None:
        await message.answer('Неверный пользователь!')
        return
    elif message.from_user.id not in users:
        users[message.from_user.id] = {
            'username': message.from_user.username,
            'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name,
            'weight': None,
            'height': None,
            'age': None,

            'selects_protein': False,
            'selects_fats': False,
            'selects_carbs': False,
        }
        await message.answer('Привет!\nМеня зовут TunWheel!')
        await message.answer('Я твой личный помощник по подсчёту калорий.\n'
                            'Я помогу тебе составить рацион питания и достичь твоих целей!')
        # Подтверждаем, что пользователь добавлен в систему
        print(f'Пользователь {message.from_user.username} добавлен в систему.')
        print(users[message.from_user.id])
    else:
        await message.answer('Привет снова!')

# Обработчик команды /help
async def help_command(message: Message):
    await message.answer('Я ваш помощник для подсчёта калорий.\n'
                        'Я могу помочь вам с подсчётом калорий и составлением рациона питания.\n'
                        'Напишите /start, чтобы начать!')

# Эхо-бот
async def echo_message(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer('Не могу отправить это сообщение.')

# Регистрация обработчиков
dp.message.register(start_command, Command(commands=['start']))
dp.message.register(help_command, Command(commands=['help']))
dp.message.register(echo_message)

# Запуск бота
if __name__ == '__main__':
    print('Бот запущен!')
    dp.run_polling(bot)