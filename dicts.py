# Здесь хранятся классы для словарей
# и их методов
from aiogram.types import Message

from typing import Dict, List, Optional, TypedDict, TypeAlias, Any

UserID: TypeAlias = int
# Переменные блюда
class DishData(TypedDict, total = False):
    name: str
    carbs: str
    protein: str
    fats: str

# Переменные пользователя
class UserInfoData(TypedDict, total = False):
    age: str
    weight: str
    height: str
    gender: str
    activity: str

class UserData(TypedDict):
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]

    user_info: UserInfoData
    custom_dishes: List[DishData]

users: Dict[UserID, UserData] = {}

def initialize_user(message: Message) -> None:
    #Инициализирует нового пользователя в системе
    if message.from_user is None:
        return

    users[message.from_user.id] = {
        # Данные пользователя
        'username': message.from_user.username,
        'first_name': message.from_user.first_name,
        'last_name': message.from_user.last_name,

        'user_info': {},
        'custom_dishes': [],
    }