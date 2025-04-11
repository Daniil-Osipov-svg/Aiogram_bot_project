from aiogram import F, Router
from aiogram.types import CallbackQuery
import logging
from dicts import users, initialize_user
from keyboards.main_menu import start_menu
from filters.filters import user_exists

router = Router()

@router.callback_query(F.data == "🥗Добавить блюда", user_exists)
@router.callback_query(F.data == "dish_no_callback", user_exists)
async def new_dish_callback(callback: CallbackQuery):
    if (callback.message is not None) and (hasattr(callback.message, 'edit_text')):
        await callback.message.edit_text('Отправьте количество углеводов в вашем блюде.')

        users[callback.from_user.id]['selects_dish'] = True
        users[callback.from_user.id]['selects_carbs'] = True
        users[callback.from_user.id]['selects_protein'] = False
        users[callback.from_user.id]['selects_fats'] = False
        users[callback.from_user.id]['selects_name'] = False

        # Сбрасываем все значения
        users[callback.from_user.id]['selects_info'] = False
        users[callback.from_user.id]['selects_age'] = False
        users[callback.from_user.id]['selects_weight'] = False
        users[callback.from_user.id]['selects_height'] = False
        # Не забудьте закрыть уведомление о нажатии кнопки
    await callback.answer()


@router.callback_query(F.data == "👀Настроить профиль", user_exists)
@router.callback_query(F.data == "user_no_callback", user_exists)
async def reuser_callback(callback: CallbackQuery):
    if (callback.message is not None) and (hasattr(callback.message, 'edit_text')):
        await callback.message.edit_text('Вы решили указать информацию о себе\nДля начала введите свой возраст.')

        users[callback.from_user.id]['selects_dish'] = False
        users[callback.from_user.id]['selects_info'] = True
        users[callback.from_user.id]['selects_age'] = True
        users[callback.from_user.id]['selects_weight'] = False
        users[callback.from_user.id]['selects_height'] = False

    await callback.answer()


@router.callback_query(F.data == "dish_yes_callback", user_exists)
@router.callback_query(F.data == "user_yes_callback", user_exists)
async def menu_callback(callback: CallbackQuery):
    if (callback.message is not None) and (hasattr(callback.message, 'edit_text')):

        # Если пользователь нажал Подтвердить создание блюда, сохраняем
        if users[callback.from_user.id]['select_is_over']:
            users[callback.from_user.id]['custom_dishes'].append({
                'name': users[callback.from_user.id]['dish_name'],
                'carbs': users[callback.from_user.id]['carbs'],
                'protein': users[callback.from_user.id]['protein'],
                'fats': users[callback.from_user.id]['fats'],
            })
            users[callback.from_user.id]['select_is_over'] = False
            users[callback.from_user.id]['selects_dish'] = False
            logging.info(users[callback.from_user.id])
        await callback.message.edit_text('Это меню. Здесь вы можете выбрать, что хотите сделать.\nВыберите один из пунктов ниже:', reply_markup=start_menu())

    await callback.answer("Данные успешно изменены")