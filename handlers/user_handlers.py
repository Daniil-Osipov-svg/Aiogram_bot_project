from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from keyboards.main_menu import start_menu, yes_or_no_user, gender_select, activity_select
import logging

from .callback_handlers import FSMFillUser
from aiogram.fsm.context import FSMContext

#База данных
from database.requests import set_user

router = Router()




@router.message(Command(commands=['start']))
async def start_command(message: Message):
    if message.from_user is not None:
        await set_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name)
        await message.answer('Привет!\nМеня зовут TunWheel!')
        await message.answer('Я твой личный помощник по подсчёту калорий.\n'
                            'Я помогу тебе составить рацион питания и достичь твоих целей!')
        await message.answer('Нажмите /help, чтобы узнать, что я умею!')
        await message.answer('Нажмите /menu, чтобы появилось меню со всеми возможностями!')

        logging.info(f'Пользователь {message.from_user.username} добавлен в систему.')
    else:
        await message.answer('Несуществующий пользователь!')
        return

@router.message(Command(commands=['menu']))
async def menu_command(message: Message):
    await message.answer(text = 'Это меню. Здесь вы можете выбрать, что хотите сделать.\nВыберите один из пунктов ниже:', reply_markup=start_menu())

@router.message(Command(commands=['help']))
async def help_command(message: Message):
    await message.answer('Я ваш помощник для подсчёта калорий.\n'
                        'Я могу помочь вам с подсчётом калорий и составлением рациона питания.\n'
                        'Напишите /start, чтобы начать!')


@router.message(F.text, StateFilter(FSMFillUser.user_age))
async def desc_user_age(message: Message, state: FSMContext):
    if message.text is not None and message.text.isdigit():

        #Проверка данных
        if float(message.text) > 120 or float(message.text) < 4:
            await message.answer('Введите ваш реальный возраст')
            return

        await state.update_data(age = message.text)

        await message.bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id - 1) #type: ignore
        await message.delete()
        await message.answer('Отправьте свой вес.')

        await state.set_state(FSMFillUser.user_weight)

    else:
        await message.answer('Введите число!')

@router.message(F.text, StateFilter(FSMFillUser.user_weight))
async def desc_user_weight(message: Message, state: FSMContext):
    if message.text is not None and message.text.isdigit():

        if float(message.text) > 645 or float(message.text) < 5.5:
            await message.answer('Введите ваш реальный вес')
            return

        await state.update_data(weight = message.text)

        await message.bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id - 1) #type: ignore
        await message.delete()
        await message.answer('Отправьте свой рост.')

        await state.set_state(FSMFillUser.user_height)

    else:
        await message.answer('Введите число!')

@router.message(F.text, StateFilter(FSMFillUser.user_height))
async def desc_user_height(message: Message, state: FSMContext):
    if message.text is not None and message.text.isdigit():

        if float(message.text) > 251 or float(message.text) < 50:
            await message.answer('Введите ваш реальный рост')
            return

        await state.update_data(height = message.text)

        await message.bot.delete_message(chat_id = message.from_user.id, message_id = message.message_id - 1) #type: ignore
        await message.delete()
        await message.answer(text = 'Выберите ваш пол.', reply_markup = gender_select())

        await state.set_state(FSMFillUser.user_gender)

    else:
        await message.answer('Введите число!')

@router.callback_query(StateFilter(FSMFillUser.user_gender))
async def desc_user_gender(callback: CallbackQuery, state: FSMContext):
    if (callback.message is not None) and (hasattr(callback.message, 'edit_text')):

        await state.update_data(gender = callback.data)

        await callback.message.edit_text(text = 'Выберите вашу среднюю физическую активность.', reply_markup = activity_select())

        await state.set_state(FSMFillUser.user_activity)

    else:
        await callback.answer()

@router.callback_query(StateFilter(FSMFillUser.user_activity))
async def desc_user_activity(callback: CallbackQuery, state: FSMContext):
    if (callback.message is not None) and (hasattr(callback.message, 'edit_text')):

        await state.update_data(activity = callback.data)
        data = await state.get_data()

        new_user_age = data.get('age', "Не указано")
        new_user_weight = data.get('weight', "Не указано")
        new_user_height = data.get('height', "Не указано")
        new_user_gender = data.get('gender', "Не указано")
        new_user_activity = data.get('activity', "Не указано")

        if new_user_activity == '⚡⚡⚡ Высокая активность ⚡⚡⚡':
            new_user_activity = '🔴Высокий🔴'
        elif new_user_activity == '⚡⚡ Средняя активность ⚡⚡':
            new_user_activity = '🟡Средний🟡'
        elif new_user_activity == '⚡ Низкая активность ⚡':
            new_user_activity = '🟢Низкий🟢'


        await callback.message.edit_text(f'Ваш возраст: {new_user_age}.\n'
                                    f'Ваш вес: {new_user_weight}.\n'
                                    f'Ваш рост: {new_user_height}.\n'
                                    f'Ваш пол: {new_user_gender}.\n'
                                    f'Ваш уровень активности: {new_user_activity}.\n'
                                    'Вы можете начать составлять рацион питания!\n\n'
                "Нажмите кнопку Подтвердить, чтобы продолжить\nИли Отмена, если хочешь подкоректировать данные о себе.",
                    reply_markup=yes_or_no_user())


        await state.set_state(FSMFillUser.end)