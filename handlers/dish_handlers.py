from aiogram import F, Router
from aiogram.types import Message
from dicts import users
from filters.filters import user_exists, selects_dish
from keyboards.main_menu import yes_or_no_dish
import logging

# Импортируем роутер
router = Router()

# Проверка на существование пользователя в сессии
router.message.filter(user_exists)

'''
@router.message(Command(commands=['new_dish']))
async def start_new_dish(message: Message):
    await message.answer('Отправьте количество углеводов в вашем блюде.')
    if message.from_user is not None:
        users[message.from_user.id]['selects_dish'] = True
        users[message.from_user.id]['selects_carbs'] = True
        users[message.from_user.id]['selects_protein'] = False
        users[message.from_user.id]['selects_fats'] = False
        users[message.from_user.id]['selects_name'] = False

        # Сбрасываем все значения
        users[message.from_user.id]['selects_info'] = False
        users[message.from_user.id]['selects_age'] = False
        users[message.from_user.id]['selects_weight'] = False
        users[message.from_user.id]['selects_height'] = False
'''


@router.message(F.text, selects_dish)
async def desc_new_dish(message: Message):
    if message.from_user is not None:
        # Проверяем, есть ли пользователь в списке
        if users[message.from_user.id]['selects_carbs']:
            # Если да, то проверяем, что он ввёл число
            if message.text is not None and message.text.isdigit():
                users[message.from_user.id]['carbs'] = message.text
                users[message.from_user.id]['selects_carbs'] = False
                users[message.from_user.id]['selects_protein'] = True
                await message.bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id - 1) #type: ignore
                await message.delete()
                await message.answer('Отправьте количество белков в вашем блюде.')
            else:
                await message.answer('Введите число!')
                print(type(message.text))
        elif users[message.from_user.id]['selects_protein']:
            if message.text is not None and message.text.isdigit():
                users[message.from_user.id]['protein'] = message.text
                users[message.from_user.id]['selects_protein'] = False
                users[message.from_user.id]['selects_fats'] = True
                await message.bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id - 1) #type: ignore
                await message.delete()
                await message.answer('Отправьте количество жиров в вашем блюде.')
            else:
                await message.answer('Введите число!')
        elif users[message.from_user.id]['selects_fats']:
            if message.text is not None and message.text.isdigit():
                users[message.from_user.id]['fats'] = message.text
                users[message.from_user.id]['selects_fats'] = False
                users[message.from_user.id]['selects_name'] = True
                await message.bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id - 1) #type: ignore
                await message.delete()
                await message.answer('Отправьте название вашего блюда.')
            else:
                await message.answer('Введите число!')
        elif users[message.from_user.id]['selects_name']:
            users[message.from_user.id]['dish_name'] = message.text
            await message.bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id - 1) #type: ignore
            await message.delete()
            await message.answer (text = f'Ваше блюдо: {users[message.from_user.id]['dish_name']}.\n'
                                f'Углеводов: {users[message.from_user.id]['carbs']}.\n'
                                f'Белков: {users[message.from_user.id]['protein']}.\n'
                                f'Жиров: {users[message.from_user.id]['fats']}.\n\n'
                                "Нажмите кнопку Подтвердить, чтобы продолжить\nИли Отмена, чтобы начать заново.",
                                reply_markup = yes_or_no_dish()
                                )
            # Сбрасываем все значения
            users[message.from_user.id]['selects_name'] = False
            users[message.from_user.id]['selects_carbs'] = False
            users[message.from_user.id]['selects_protein'] = False
            users[message.from_user.id]['selects_fats'] = False
            users[message.from_user.id]['select_is_over'] = True
    else:
        await message.answer('Несуществующее выражение!')
        return