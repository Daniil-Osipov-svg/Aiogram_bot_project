# Импортируем файлы проекта
from dicts import *

# Импортируем библиотеки
from aiogram import F #noqa
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, ChatMemberUpdatedFilter, KICKED #noqa
from aiogram.types import Message, ChatMemberUpdated #noqa

#API моего чат бота
BOT_TOKEN = '7774687817:AAGlmbpI-HhrXadQsgu5LyWqNKlsOcEAx9E'


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Проверка на наличие пользователя в списке
def user_exists(message):
    return message.from_user.id in users
def user_not_exists(message):
    return not user_exists(message)

# Обработчик команды /start
@dp.message(Command(commands=['start']))
async def start_command(message: Message):
    # Проверяем, есть ли пользователь в списке
    # Если нет, добавляем его

    # Убираем срабатывание ошибки mypy
    if message.from_user is not None:
        # Инициализируем пользователя
        initialize_user(message)
        await message.answer('Привет!\nМеня зовут TunWheel!')
        await message.answer('Я твой личный помощник по подсчёту калорий.\n'
                            'Я помогу тебе составить рацион питания и достичь твоих целей!')
        # Подтверждаем, что пользователь добавлен в систему
        print(f'Пользователь {message.from_user.username} добавлен в систему.')
        print(users[message.from_user.id])
    else:
        await message.answer('Несуществующий пользователь!')
        return

# Обработчик команды /help
@dp.message(Command(commands=['help']))
async def help_command(message: Message):
    await message.answer('Я ваш помощник для подсчёта калорий.\n'
                        'Я могу помочь вам с подсчётом калорий и составлением рациона питания.\n'
                        'Напишите /start, чтобы начать!')

# Обработчик команды /new_dish
@dp.message(Command(commands=['new_dish']), user_exists)
async def start_new_dish(message: Message):
    await message.answer('Отправьте количество углеводов в вашем блюде.')
    if message.from_user is not None:
        users[message.from_user.id]['selects_dish'] = True
        users[message.from_user.id]['selects_carbs'] = True
        users[message.from_user.id]['selects_protein'] = False
        users[message.from_user.id]['selects_fats'] = False
        users[message.from_user.id]['selects_name'] = False

# Составление нового блюда
@dp.message(F.text, user_exists)
async def desc_new_dish(message: Message):
    if message.from_user is not None:
        # Проверяем, есть ли пользователь в списке
        if users[message.from_user.id]['selects_dish']:
            # Если да, то проверяем, что он ввёл число
            if message.text is not None and message.text.isdigit():
                users[message.from_user.id]['carbs'] = message.text
                users[message.from_user.id]['selects_dish'] = False
                users[message.from_user.id]['selects_protein'] = True
                await message.answer('Отправьте количество белков в вашем блюде.')
            else:
                await message.answer('Введите число!')
                print(type(message.text))
        elif users[message.from_user.id]['selects_protein']:
            if message.text is not None and message.text.isdigit():
                users[message.from_user.id]['protein'] = message.text
                users[message.from_user.id]['selects_protein'] = False
                users[message.from_user.id]['selects_fats'] = True
                await message.answer('Отправьте количество жиров в вашем блюде.')
            else:
                await message.answer('Введите число!')
        elif users[message.from_user.id]['selects_fats']:
            if message.text is not None and message.text.isdigit():
                users[message.from_user.id]['fats'] = message.text
                users[message.from_user.id]['selects_fats'] = False
                users[message.from_user.id]['selects_name'] = True
                await message.answer('Отправьте название вашего блюда.')
            else:
                await message.answer('Введите число!')
        elif users[message.from_user.id]['selects_name']:
            users[message.from_user.id]['dish_name'] = message.text
            await message.answer(f'Ваше блюдо: {users[message.from_user.id]['dish_name']}.\n'
                                f'Углеводов: {users[message.from_user.id]['carbs']}.\n'
                                f'Белков: {users[message.from_user.id]['protein']}.\n'
                                f'Жиров: {users[message.from_user.id]['fats']}.\n\n'
                                "Отправьте любое сообщение, чтобы сохранить блюдо.\n"
                                )
            # Сбрасываем все значения
            users[message.from_user.id]['selects_name'] = False
            users[message.from_user.id]['selects_dish'] = False
            users[message.from_user.id]['selects_protein'] = False
            users[message.from_user.id]['selects_fats'] = False
            users[message.from_user.id]['select_is_over'] = True
        elif users[message.from_user.id]['select_is_over']:
            # Если пользователь ввёл любое сообщение, то мы сохраняем его в список
            users[message.from_user.id]['custom_dishes'].append({
                'name': users[message.from_user.id]['dish_name'],
                'carbs': users[message.from_user.id]['carbs'],
                'protein': users[message.from_user.id]['protein'],
                'fats': users[message.from_user.id]['fats'],
            })
            users[message.from_user.id]['select_is_over'] = False
            print(users[message.from_user.id])
            await message.answer('Вы завершили создание блюда.\n'
                                'Напишите /new_dish, чтобы создать новое блюдо.')
    else:
        await message.answer('Несуществующее выражение!')
        return

@dp.message(user_not_exists)
async def say_no_user(message: Message):
    await message.answer('Вы отсутствуете в нынешнем сеансе.\n'
                        'Напишите /start, чтобы продолжить!')
# Запуск бота
if __name__ == '__main__':
    print('Бот запущен!')
    dp.run_polling(bot)