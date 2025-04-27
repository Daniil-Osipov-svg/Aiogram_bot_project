from aiogram import F, Router
from aiogram.types import CallbackQuery
from dicts import users
from filters.filters import user_exists
from keyboards.main_menu import start_menu, return_select
from database.requests import get_user_info, add_user_info

router = Router()

router.message.filter(user_exists)

def calculate_tdee(age, weight, height, gender, activity) -> float:
    # Формула Миффлина-Сан Жеора
    bmr = 10 * float(weight) + 6.25 * float(height) - 5 * float(age) + (200 if gender == 'муж' else 50)

    factors = {'низкая': 1.3, 'средняя': 1.55, 'высокая': 1.9}
    return bmr * factors.get(activity, 1.2)

@router.callback_query(F.data == '🕗Моя суточная норма')
async def cmd_tdee(callback: CallbackQuery):
    uid = callback.from_user.id

    user_info = await get_user_info(uid)

    if not user_info:
        await callback.answer("Пожалуйста, сначала заполните информацию о себе.")
        return

    # Сохраняем TDEE в бд пользователей

    #users[uid]['user_info']["tdee"] = f"{tdee:.2f}"

    text = (
        f"Ваш суточный расход калорий (TDEE): {user_info.tdee:.2f} ккал.\n"
        "Это количество калорий, которое вам нужно для поддержания текущего веса."
        "Чтобы сбросить вес, вам нужно создать дефицит калорий.\n"
        "И чтобы набрать вес, вам нужно наоборот создать избыток калорий. Желательно в пределах 200-400 ккал.\n"
    )

    if (callback.message is not None) and (hasattr(callback.message, 'edit_text')):
        await callback.message.edit_text(text=text, reply_markup=return_select())

@router.callback_query(F.data == '🔙Вернуться в меню')
async def return_menu_command(callback: CallbackQuery):
    if (callback.message is not None) and (hasattr(callback.message, 'edit_text')):
        await callback.message.edit_text(text = 'Это меню. Здесь вы можете выбрать, что хотите сделать.\nВыберите один из пунктов ниже:', reply_markup=start_menu())
