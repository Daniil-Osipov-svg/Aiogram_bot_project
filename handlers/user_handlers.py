from aiogram import F, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from dicts import users, initialize_user

def user_exists(message):
    return message.from_user is not None and message.from_user.id in users

def user_not_exists(message):
    return not user_exists(message)

def selects_info(message):
    return message.from_user is not None and message.from_user.id in users and users[message.from_user.id]['selects_info']

def register_user_handlers(dp: Dispatcher):
    """Регистрирует обработчики команд для работы с пользователями"""

    @dp.message(Command(commands=['start']))
    async def start_command(message: Message):
        if message.from_user is not None:
            initialize_user(message)
            await message.answer('Привет!\nМеня зовут TunWheel!')
            await message.answer('Я твой личный помощник по подсчёту калорий.\n'
                               'Я помогу тебе составить рацион питания и достичь твоих целей!')
            print(f'Пользователь {message.from_user.username} добавлен в систему.')
        else:
            await message.answer('Несуществующий пользователь!')
            return

    @dp.message(Command(commands=['help']))
    async def help_command(message: Message):
        await message.answer('Я ваш помощник для подсчёта калорий.\n'
                           'Я могу помочь вам с подсчётом калорий и составлением рациона питания.\n'
                           'Напишите /start, чтобы начать!')

    @dp.message(Command(commands=['reuser']), user_exists)
    async def reuser_command(message: Message):
        await message.answer('Вы решили указать информацию о себе\nДля начала введите свой возраст.')
        if message.from_user is not None:
            users[message.from_user.id]['selects_dish'] = False
            users[message.from_user.id]['selects_info'] = True
            users[message.from_user.id]['selects_age'] = True
            users[message.from_user.id]['selects_weight'] = False
            users[message.from_user.id]['selects_height'] = False

    @dp.message(F.text, selects_info)
    async def desc_user_info(message: Message):
        if message.from_user is not None:
            # Проверяем, есть ли пользователь в списке
            if users[message.from_user.id]['selects_age']:
                # Если да, то проверяем, что он ввёл число
                if message.text is not None and message.text.isdigit():
                    users[message.from_user.id]['age'] = message.text
                    users[message.from_user.id]['selects_age'] = False
                    users[message.from_user.id]['selects_weight'] = True
                    await message.answer('Отправьте свой вес.')
                else:
                    await message.answer('Введите число!')
            elif users[message.from_user.id]['selects_weight']:
                if message.text is not None and message.text.isdigit():
                    users[message.from_user.id]['weight'] = message.text
                    users[message.from_user.id]['selects_weight'] = False
                    users[message.from_user.id]['selects_height'] = True
                    await message.answer('Отправьте свой рост.')
                else:
                    await message.answer('Введите число!')
            elif users[message.from_user.id]['selects_height']:
                if message.text is not None and message.text.isdigit():
                    users[message.from_user.id]['height'] = message.text
                    users[message.from_user.id]['selects_height'] = False
                    users[message.from_user.id]['selects_info'] = False

                    await message.answer(f'Ваш возраст: {users[message.from_user.id]["age"]}.\n'
                                        f'Ваш вес: {users[message.from_user.id]["weight"]}.\n'
                                        f'Ваш рост: {users[message.from_user.id]["height"]}.\n\n'
                                        'Вы можете начать составлять рацион питания!\n\n')
                    await message.answer('Нажмите /reuser если вы хотите ещё раз ввести данные')
                else:
                    await message.answer('Введите число!')
        else:
            await message.answer('Несуществующее выражение!')
            return

    @dp.message(user_not_exists)
    async def say_no_user(message: Message):
        await message.answer('Вы отсутствуете в нынешнем сеансе.\n'
                           'Напишите /start, чтобы продолжить!')