from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message
from keyboards.main_menu import yes_or_no_dish
from filters.filters import user_exists, selects_dish

from .callback_handlers import FSMFillDish
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state

# Импортируем роутер
router = Router()

# Проверка на существование пользователя в сессии
router.message.filter(user_exists)


@router.message(F.text, StateFilter(FSMFillDish.dish_carbs))
async def desc_new_dish_carbs(message: Message, state: FSMContext):
    if message.text is not None and message.text.isdigit():

        await state.update_data(carbs = message.text)

        await message.bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id - 1) #type: ignore
        await message.delete()
        await message.answer('Отправьте количество белков (грамм) в вашем блюде.')

        await state.set_state(FSMFillDish.dish_protein)
    else:
        await message.delete()
        await message.answer('Введите число!')

@router.message(F.text, StateFilter(FSMFillDish.dish_protein))
async def desc_new_dish_protein(message: Message, state: FSMContext):
    if message.text is not None and message.text.isdigit():

        await state.update_data(protein = message.text)

        await message.bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id - 1) #type: ignore
        await message.delete()
        await message.answer('Отправьте количество жиров (грамм) в вашем блюде.')

        await state.set_state(FSMFillDish.dish_fats)
    else:
        await message.delete()
        await message.answer('Введите число!')

@router.message(F.text, StateFilter(FSMFillDish.dish_fats))
async def desc_new_dish_fats(message: Message, state: FSMContext):
    if message.text is not None and message.text.isdigit():

        await state.update_data(fats = message.text)

        await message.bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id - 1) #type: ignore
        await message.delete()
        await message.answer('Отправьте название вашего блюда.')

        await state.set_state(FSMFillDish.dish_name)
    else:
        await message.delete()
        await message.answer('Введите число!')

@router.message(F.text, StateFilter(FSMFillDish.dish_name))
async def desc_new_dish_name(message: Message, state: FSMContext):
    if message.text is not None:

        await state.update_data(name = message.text)
        data = await state.get_data()

        new_dish_name = data.get('name', "Не указано")
        new_dish_carbs = data.get('carbs', "Не указано")
        new_dish_protein = data.get('protein', "Не указано")
        new_dish_fats = data.get('fats', "Не указано")

        await message.bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id - 1) #type: ignore
        await message.delete()
        await message.answer (text = f'Ваше блюдо: {new_dish_name}.\n'
                                  f'Углеводов: {new_dish_carbs}.\n'
                                  f'Белков: {new_dish_protein}.\n'
                                  f'Жиров: {new_dish_fats}.\n\n'
                                "Нажмите кнопку Подтвердить, чтобы продолжить\nИли Отмена, чтобы начать заново.",
                                reply_markup = yes_or_no_dish()
                            )

        await state.set_state(FSMFillDish.end)

    else:
        await message.answer('Несуществующее выражение!')
        return