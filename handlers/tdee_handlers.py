from aiogram import F, Router
from aiogram.types import CallbackQuery
from dicts import users
from filters.filters import user_exists
from keyboards.main_menu import start_menu, return_select

router = Router()

router.message.filter(user_exists)

def calculate_tdee(user_info) -> float:
    # Формула Миффлина-Сан Жеора
    weight = float(user_info['weight'])
    height = float(user_info['height'])
    age = float(user_info['age'])
    gender = user_info['gender']
    bmr = 10 * weight + 6.25 * height - 5 * age + (200 if gender == 'муж' else 50)

    factors = {'низкая': 1.3, 'средняя': 1.55, 'высокая': 1.9}
    return bmr * factors.get(user_info['activity'], 1.2)

@router.callback_query(F.data == '🕗Моя суточная норма')
async def cmd_tdee(callback: CallbackQuery):
    uid = callback.from_user.id
    if uid not in users or not users[uid]['user_info']:
        await callback.answer("Пожалуйста, сначала заполните информацию о себе.")
        return

    tdee = calculate_tdee(users[uid]['user_info'])

    # Сохраняем TDEE в бд пользователей

    users[uid]['user_info']["tdee"] = f"{tdee:.2f}"

    text = (
        f"Ваш суточный расход калорий (TDEE): {tdee:.2f} ккал.\n"
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
