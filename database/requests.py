from database.models import async_session
from database.models import User, UserInfo, Dish
from sqlalchemy import select, update, delete


async def set_user(tg_id, first_name, last_name):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            user = User(tg_id=tg_id, first_name=first_name, last_name=last_name)
            session.add(user)
            await session.commit()
        return user



async def add_user_info(user_id: int, age: int, weight: int, height: int, gender: str, activity: str):
    async with async_session() as session:
        result = await session.execute(select(UserInfo).where(UserInfo.user_id == user_id))
        info = result.scalar_one_or_none()
        if info:
            # Обновляем существующую запись
            info.age = age
            info.weight = weight
            info.height = height
            info.gender = gender
            info.activity = activity
        else:
            # Создаём новую запись
            info = UserInfo(
                user_id=user_id,
                age=age,
                weight=weight,
                height=height,
                gender=gender,
                activity=activity
            )
            session.add(info)
        await session.commit()
        return info