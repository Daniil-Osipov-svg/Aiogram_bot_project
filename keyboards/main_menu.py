from typing import List
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dicts import DishData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.create_keyboard import create_keyboard


def start_menu() -> InlineKeyboardMarkup:

    reply_markup = create_keyboard(
        2,
        "🥗Добавить блюда", "🥙Мои блюда",
        "👀Настроить профиль", "⚖Расчитать BMI",
        "🕗Моя суточная норма", "⌛Рацион на день",
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

ITEMS_PER_PAGE = 5  # Количество элементов на странице

def make_menu(dishes: List[DishData], page: int, selected: List[DishData]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    start = page * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE

    # Кнопки блюд
    for idx, dish in enumerate(dishes[start:end], start=start):
        checked = "✅" if dish in selected else ""
        text = f"{checked} {dish['name']}"
        callback = f"toggle:{idx}:{page}"
        kb.button(text=text, callback_data=callback)

    kb.adjust(2)

    # Кнопки навигации

    nav_buttons = []

    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="<", callback_data=f"page:{page-1}"))

    if end < len(dishes):
        nav_buttons.append(InlineKeyboardButton(text=">", callback_data=f"page:{page+1}"))

    if nav_buttons:
        kb.row(*nav_buttons)

    kb.row(InlineKeyboardButton(text="Подтвердить ✅", callback_data="confirm"))

    return kb.as_markup()


def delete_menu(dishes: List[DishData], page: int, selected: List[DishData]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    start = page * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE

    # Кнопки блюд
    for idx, dish in enumerate(dishes[start:end], start=start):
        checked = "❌" if dish in selected else ""
        text = f"{checked} {dish['name']} - {dish['carbs']} угл, {dish["protein"]} бел, {dish['fats']} жир"
        callback = f"delete_toggle:{idx}:{page}"
        kb.button(text=text, callback_data=callback)

    kb.adjust(1)

    # Кнопки навигации

    nav_buttons = []

    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="<", callback_data=f"delete_page:{page-1}"))

    if end < len(dishes):
        nav_buttons.append(InlineKeyboardButton(text=">", callback_data=f"delete_page:{page+1}"))

    if nav_buttons:
        kb.row(*nav_buttons)

    kb.row(InlineKeyboardButton(text="Подтвердить ✅", callback_data="delete_confirm"))

    return kb.as_markup()







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