from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.create_keyboard import create_keyboard


def start_menu() -> InlineKeyboardMarkup:

    reply_markup = create_keyboard(
        2,
        "🥗Добавить блюда", "🥙Мои блюда",
        "👀Настроить профиль", "👴Помощь",
        "Моя суточная норма", "Настройки",
    )

    return reply_markup


def yes_or_no_user() -> InlineKeyboardMarkup:

    reply_markup = create_keyboard(
        1,
        user_yes_callback = "✅Подтвердить",
        user_no_callback = "❌Отмена",
    )

    return reply_markup


def yes_or_no_dish() -> InlineKeyboardMarkup:

    reply_markup = create_keyboard(
        1,
        dish_yes_callback = "✅Подтвердить",
        dish_no_callback = "❌Отмена",
    )

    return reply_markup


def gender_select() -> InlineKeyboardMarkup:

    reply_markup = create_keyboard(
        2,
        "♂ Мужской ♂",
        "♀ Женский ♀",
    )

    return reply_markup


def activity_select() -> InlineKeyboardMarkup:

    reply_markup = create_keyboard(
        1,
        "⚡⚡⚡ Высокая активность ⚡⚡⚡",
        "⚡⚡ Средняя активность ⚡⚡",
        "⚡ Низкая активность ⚡",
    )

    return reply_markup

def return_select() -> InlineKeyboardMarkup:

    reply_markup = create_keyboard(
        1,
        "🔙Вернуться в меню",
    )

    return reply_markup











# ЭТО ДЛЯ ТЕСТА
all_user_dishes = {
    1: "Блюдо 1",
    2: "Блюдо 2",
    3: "Блюдо 3",
    4: "Блюдо 4",
    5: "Блюдо 5",
    6: "Блюдо 6",
}

def pagination_keyboard(page = 1):

    middle_button = f"{page}/{len(all_user_dishes)/5}"

    if page == 1:
        return pagination_keyboard(middle_button, ">")
    elif page == len(all_user_dishes):
        return pagination_keyboard("<" ,middle_button)
    else:
        return pagination_keyboard("<", middle_button, ">")




if __name__ == "__main__":
    # Пример использования функции
    keyboard = start_menu()
    print(keyboard)  # Вывод клавиатуры для проверки