from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message
from keyboards.main_menu import yes_or_no_dish

from .callback_handlers import FSMFillDish
from aiogram.fsm.context import FSMContext

# Импортируем роутер
router = Router()


@router.message(F.text, StateFilter(FSMFillDish.dish_carbs))
async def desc_new_dish_carbs(message: Message, state: FSMContext):
    if message.text is not None and message.text.isdigit():

        if float(message.text) > 10000:
            await message.answer('Слишком много грамм в блюде!')
            return

        if float(message.text) < 0:
            await message.answer('Значение не может быть отрицательным!')
            return

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

        if float(message.text) > 10000:
            await message.answer('Слишком много грамм в блюде!')
            return

        if float(message.text) < 0:
            await message.answer('Значение не может быть отрицательным!')
            return

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

        if float(message.text) > 10000:
            await message.answer('Слишком много грамм в блюде!')
            return

        if float(message.text) < 0:
            await message.answer('Значение не может быть отрицательным!')
            return

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

        if len(message.text) > 40:
            await message.answer('Название блюда не должно превышать 40 символов')
            return

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