# Здесь хранятся классы для словарей
# и их методов
from aiogram.types import Message

from typing import Dict, List, Tuple, Union, Optional, TypedDict

class DishData(TypedDict):
    name: Optional[str]
    carbs: Optional[str]
    protein: Optional[str]
    fats: Optional[str]

class UserData(TypedDict):
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    weight: Optional[str]
    height: Optional[str]
    age: Optional[str]
    selects_name: bool
    selects_dish: bool
    selects_protein: bool
    selects_fats: bool
    selects_carbs: bool
    select_is_over: bool
    carbs: Optional[str]
    protein: Optional[str]
    fats: Optional[str]
    dish_name: Optional[str]
    custom_dishes: List[DishData]

users: Dict[int, UserData] = {}

def initialize_user(message: Message) -> None:
    #Инициализирует нового пользователя в системе
    if message.from_user is None:
        return

    users[message.from_user.id] = {
        'username': message.from_user.username,
        'first_name': message.from_user.first_name,
        'last_name': message.from_user.last_name,
        'weight': None,
        'height': None,
        'age': None,

        'selects_name': False,
        'selects_dish': False,
        'selects_protein': False,
        'selects_fats': False,
        'selects_carbs': False,
        'select_is_over': False,

        'carbs': None,
        'protein': None,
        'fats': None,
        'dish_name': None,

        'custom_dishes': [],
    }