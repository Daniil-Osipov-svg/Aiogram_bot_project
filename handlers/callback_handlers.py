from aiogram import F, Router
from aiogram.types import CallbackQuery
from typing import cast
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.storage.redis import RedisStorage
import logging

from dicts import users, DishData, UserInfoData, UserData
from keyboards.main_menu import start_menu
from filters.filters import user_exists

class FSMFillDish(StatesGroup):
    dish_carbs = State()
    dish_protein = State()
    dish_fats = State()
    dish_name = State()

    end = State()

class FSMFillUser(StatesGroup):
    user_age = State()
    user_weight = State()
    user_height = State()
    user_gender = State()
    user_activity = State()

    end = State()

router = Router()

@router.callback_query(F.data.in_(["dish_no_callback", "🥗Добавить блюда"]))
async def new_dish_callback(callback: CallbackQuery, state: FSMContext):
    if (callback.message is not None) and (hasattr(callback.message, 'edit_text')):
        await callback.message.edit_text('Отправьте количество углеводов в вашем блюде.')
        await state.clear()
        await state.set_state(FSMFillDish.dish_carbs)
    else:
        await callback.answer()


@router.callback_query(F.data.in_(["user_no_callback", "👀Настроить профиль"]), user_exists)
async def reuser_callback(callback: CallbackQuery, state: FSMContext):
    if (callback.message is not None) and (hasattr(callback.message, 'edit_text')):
        await callback.message.edit_text('Вы решили указать информацию о себе\nДля начала введите свой возраст.')
        await state.clear()
        await state.set_state(FSMFillUser.user_age)

    else:
        await callback.answer()


@router.callback_query(F.data == "dish_yes_callback", StateFilter(FSMFillDish.end), user_exists)
async def dish_menu_callback(callback: CallbackQuery, state: FSMContext):
    if (callback.message is not None) and (hasattr(callback.message, 'edit_text')):

        user_id = callback.from_user.id

        data = await state.get_data()
        dish_data = cast(DishData, data)

        # Если пользователь нажал Подтвердить создание блюда, сохраняем
        users[user_id]['custom_dishes'].append(dish_data)

        await state.clear()

        logging.info(users[callback.from_user.id])
        await callback.message.edit_text('Это меню. Здесь вы можете выбрать, что хотите сделать.\nВыберите один из пунктов ниже:', reply_markup=start_menu())

    await callback.answer("Блюдо успешно добавлено!")

@router.callback_query(F.data == "user_yes_callback", StateFilter(FSMFillUser.end), user_exists)
async def user_menu_callback(callback: CallbackQuery, state: FSMContext):
    if (callback.message is not None) and (hasattr(callback.message, 'edit_text')):

        user_id = callback.from_user.id

        user_data = await state.get_data()
        info_data = cast(UserInfoData, user_data)

        # Если пользователь нажал Подтвердить пользователя, сохраняем
        users[user_id]['user_info'] = info_data

        await state.clear()

        logging.info(users[callback.from_user.id])
        await callback.message.edit_text('Это меню. Здесь вы можете выбрать, что хотите сделать.\nВыберите один из пунктов ниже:', reply_markup=start_menu())

    await callback.answer("Данные пользователя успешно обновлены!")