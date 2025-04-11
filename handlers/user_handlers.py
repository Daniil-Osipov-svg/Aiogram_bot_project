from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from dicts import users, initialize_user
from keyboards.main_menu import start_menu, yes_or_no_user
from filters.filters import user_exists, user_not_exists, selects_info
import logging

router = Router()




@router.message(Command(commands=['start']))
async def start_command(message: Message):
    if message.from_user is not None:
        initialize_user(message)
        await message.answer('Привет!\nМеня зовут TunWheel!')
        await message.answer('Я твой личный помощник по подсчёту калорий.\n'
                            'Я помогу тебе составить рацион питания и достичь твоих целей!')
        await message.answer('Нажмите /help, чтобы узнать, что я умею!')
        await message.answer('Нажмите /menu, чтобы появилось меню со всеми возможностями!')

        logging.info(f'Пользователь {message.from_user.username} добавлен в систему.')
    else:
        await message.answer('Несуществующий пользователь!')
        return

@router.message(Command(commands=['menu']), user_exists)
async def menu_command(message: Message):
    await message.answer(text = 'Это меню. Здесь вы можете выбрать, что хотите сделать.\nВыберите один из пунктов ниже:', reply_markup=start_menu())

@router.message(Command(commands=['help']))
async def help_command(message: Message):
    await message.answer('Я ваш помощник для подсчёта калорий.\n'
                        'Я могу помочь вам с подсчётом калорий и составлением рациона питания.\n'
                        'Напишите /start, чтобы начать!')


'''
@router.message(Command(commands=['reuser']), user_exists)
async def reuser_command(message: Message):
    await message.answer('Вы решили указать информацию о себе\nДля начала введите свой возраст.')
    if message.from_user is not None:
        users[message.from_user.id]['selects_dish'] = False
        users[message.from_user.id]['selects_info'] = True
        users[message.from_user.id]['selects_age'] = True
        users[message.from_user.id]['selects_weight'] = False
        users[message.from_user.id]['selects_height'] = False
'''

@router.message(F.text, selects_info)
async def desc_user_info(message: Message):
    if message.from_user is not None:
        # Проверяем, есть ли пользователь в списке
        if users[message.from_user.id]['selects_age']:
            # Если да, то проверяем, что он ввёл число
            if message.text is not None and message.text.isdigit():
                users[message.from_user.id]['age'] = message.text
                users[message.from_user.id]['selects_age'] = False
                users[message.from_user.id]['selects_weight'] = True
                await message.bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id - 1) #type: ignore
                await message.delete()
                await message.answer('Отправьте свой вес.')
            else:
                await message.answer('Введите число!')
        elif users[message.from_user.id]['selects_weight']:
            if message.text is not None and message.text.isdigit():
                users[message.from_user.id]['weight'] = message.text
                users[message.from_user.id]['selects_weight'] = False
                users[message.from_user.id]['selects_height'] = True
                await message.bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id - 1) #type: ignore
                await message.delete()
                await message.answer('Отправьте свой рост.')
            else:
                await message.answer('Введите число!')
        elif users[message.from_user.id]['selects_height']:
            if message.text is not None and message.text.isdigit():
                users[message.from_user.id]['height'] = message.text
                users[message.from_user.id]['selects_height'] = False
                users[message.from_user.id]['selects_info'] = False

                await message.bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id - 1) #type: ignore
                await message.delete()

                await message.answer(f'Ваш возраст: {users[message.from_user.id]["age"]}.\n'
                                    f'Ваш вес: {users[message.from_user.id]["weight"]}.\n'
                                    f'Ваш рост: {users[message.from_user.id]["height"]}.\n\n'
                                    'Вы можете начать составлять рацион питания!\n\n'
                "Нажмите кнопку Подтвердить, чтобы продолжить\nИли Отмена, если хочешь подкоректировать данные о себе.",
                    reply_markup=yes_or_no_user())
            else:
                await message.answer('Введите число!')
    else:
        await message.answer('Несуществующее выражение!')
        return

@router.message(user_not_exists)
async def say_no_user(message: Message):
    await message.answer('Вы отсутствуете в нынешнем сеансе.\n'
                        'Напишите /start, чтобы продолжить!')