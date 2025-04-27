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



async def add_user_info(user_id: int, age: int, weight: int, height: int, gender: str, activity: str, tdee: float):
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
            info.tdee = tdee
        else:
            # Создаём новую запись
            info = UserInfo(
                user_id=user_id,
                age=age,
                weight=weight,
                height=height,
                gender=gender,
                activity=activity,
                tdee = tdee
            )
            session.add(info)
        await session.commit()
        return info


async def add_dish(user_id, dish_name, carbs, proteins, fats):
    async with async_session() as session:
        dish = Dish(
            user_id = user_id,
            dish_name = dish_name,
            carbs = carbs,
            proteins = proteins,
            fats = fats
        )
        session.add(dish)
        await session.commit()
        return dish


async def get_user_info(user_id):
    async with async_session() as session:
        result = await session.execute(select(UserInfo).where(User.tg_id == user_id))
        info = result.scalar_one_or_none()

        return info


async def get_user_dishes(user_id):
    async with async_session() as session:
        result = await session.execute(select(Dish).where(Dish.user_id == user_id))
        return result.scalars().all()


async def delete_dishes(user_id, dish_names):
    async with async_session() as session:
        await session.execute(
            delete(Dish).where(Dish.user_id == user_id, Dish.dish_name.in_(dish_names))
        )
        await session.commit()