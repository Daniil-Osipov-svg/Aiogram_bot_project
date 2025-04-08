from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from dicts import users

# Импортируем роутер
router = Router()

def selects_dish(message):
    return message.from_user is not None and message.from_user.id in users and users[message.from_user.id]['selects_dish']

def user_exists(message):
    return message.from_user is not None and message.from_user.id in users


@router.message(Command(commands=['new_dish']), user_exists)
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
            users[message.from_user.id]['selects_carbs'] = False
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
            users[message.from_user.id]['selects_dish'] = False
            print(users[message.from_user.id])
            await message.answer('Вы завершили создание блюда.\n'
                                'Напишите /new_dish, чтобы создать новое блюдо.')
    else:
        await message.answer('Несуществующее выражение!')
        return