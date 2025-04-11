from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def create_keyboard(width: int, *args: str, **kwargs: str) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    buttons = []

    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(text = button, callback_data = button))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(text = text, callback_data = button))

    kb_builder.row(*buttons, width=width)
    kb = kb_builder.as_markup()

    return kb

if __name__ == "__main__":
    # Пример использования функции
    keyboard = create_keyboard(2, Button3="Button3", Button4="Button4")
    print(keyboard)  # Вывод клавиатуры для проверки