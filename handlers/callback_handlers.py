from aiogram import F, Router
from aiogram.types import CallbackQuery
from typing import cast
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import logging

from dicts import users, DishData, UserInfoData
from handlers.tdee_handlers import calculate_tdee
from keyboards.main_menu import start_menu, make_menu, return_select, delete_menu
from filters.filters import user_exists
from database.requests import add_user_info

# FSM данных о новом блюде
class FSMFillDish(StatesGroup):
    dish_carbs = State()
    dish_protein = State()
    dish_fats = State()
    dish_name = State()

    end = State()

# FSM данных о состоянии пользователя
class FSMFillUser(StatesGroup):
    user_age = State()
    user_weight = State()
    user_height = State()
    user_gender = State()
    user_activity = State()

    end = State()

# FSM данных о добавленных блюдах
class FSMDietState(StatesGroup):
    selecting = State()

class FSMDeleteState(StatesGroup):
    deleting = State()

router = Router()

@router.callback_query(F.data == "⚖Расчитать BMI")
async def give_advice(callback: CallbackQuery):
    uid = callback.from_user.id
    data = users.get(uid)
    if not data or not data['user_info']:
        await callback.answer("Сначала заполните информацию о себе командой «Добавить инфо».")
        return

    ui = data['user_info']
    # Расчёт BMI
    try:
        weight = float(ui['weight'])
        height = float(ui['height'])
        bmi = weight / ((height / 100) ** 2)
    except (KeyError, ValueError, ZeroDivisionError):
        await callback.answer("Неверные данные роста/веса. Пожалуйста, обновите информацию.")
        return

    # Расчёт TDEE
    tdee = calculate_tdee(ui)

    # Определяем статус по BMI
    if bmi < 18.5:
        status = "недостаточный вес"
        recommendation = (
            "Рекомендую увеличить калорийность рациона на 10–20% за счёт углеводов и белков, "
            "добавить 2–3 приёма пищи и уделить внимание силовым тренировкам для набора массы."
        )
    elif bmi < 25:
        status = "нормальный вес"
        recommendation = (
            "Ваш вес в норме. Поддерживайте текущий режим питания и тренировок. "
            "При желании скорректировать форму — слегка уменьшите калорийность или замените часть углеводов на белок."
        )
    else:
        status = "избыточный вес"
        recommendation = (
            "Рекомендую создать дефицит калорий 10–15% от TDEE, увеличить кардионагрузку "
            "и контролировать размеры порций. Уделите внимание белковому питанию и клетчатке."
        )

    text = (
        f"📊 *Ваши показатели:*\n\n"
        f"- BMI: {bmi:.1f} ({status})\n"
        f"- Суточная норма калорий (TDEE): {tdee:.0f} ккал\n\n"
        f"*Совет:* {recommendation}"
    )
    if (callback.message is not None) and (hasattr(callback.message, 'edit_text')):
        await callback.message.edit_text(text=text, reply_markup=return_select(), parse_mode="Markdown")



# Удаление блюда

@router.callback_query(F.data == "🥙Мои блюда")
async def show_delete(callback: CallbackQuery, state: FSMContext):
    uid = callback.from_user.id

    await state.clear()

    try: dishes = users[uid]['custom_dishes']

    except KeyError:
        await callback.answer("Пожалуйста, сначала добавьте блюда.")
        return

    if not dishes or len(dishes) == 0:
        await callback.answer("У вас нет добавленных блюд.")
        return

    await state.clear()

    await state.update_data(dishes=dishes, page=0, selected=[])

    kb = delete_menu(dishes, page=0, selected=[])
    if (callback.message is not None) and (hasattr(callback.message, 'edit_text')):
        await callback.message.edit_text("Выберите блюдо из списка ниже, чтобы удалить его:", reply_markup=kb)

    await state.set_state(FSMDeleteState.deleting)

# Выбор блюда для удаления
@router.callback_query(lambda c: c.data and c.data.startswith("delete_toggle:") , FSMDeleteState.deleting)
async def toggle_delete(callback: CallbackQuery, state: FSMContext):
    if callback.data is None:
        await callback.answer("Неверные данные callback")
        return

    data = await state.get_data()
    dishes, sel, page = data.get("dishes"), data.get("selected"), data.get("page")
    _, idx_str, _ = callback.data.split(":")
    idx = int(idx_str)
    dish = dishes[idx] #type: ignore

    if dish in sel: #type: ignore
        sel.remove(dish) #type: ignore
    else:
        sel.append(dish) #type: ignore

    await state.update_data(selected=sel)

    kb = delete_menu(dishes, page, sel) #type: ignore
    if (callback.message is not None) and (hasattr(callback.message, 'edit_text')):
        await callback.message.edit_text("Выберите блюдо из списка ниже, чтобы удалить его:", reply_markup=kb)

    await callback.answer()

@router.callback_query(lambda c: c.data and c.data.startswith("page:"), FSMDeleteState.deleting)
async def change_delete_page(callback: CallbackQuery, state: FSMContext):

    if callback.data is None:
        await callback.answer("Неверные данные callback")
        return

    data = await state.get_data()
    dishes, sel = data['dishes'], data['selected']
    page = int(callback.data.split(":")[1])
    await state.update_data(page=page)
    kb = delete_menu(dishes, page, sel)
    if (callback.message is not None) and (hasattr(callback.message, 'edit_text')):
        await callback.message.edit_text("Выберите блюдо из списка ниже, чтобы удалить его:", reply_markup=kb)
    await callback.answer()

@router.callback_query(F.data == "delete_confirm", FSMDeleteState.deleting)
async def confirm_delete(callback: CallbackQuery, state: FSMContext):
    uid = callback.from_user.id
    data = await state.get_data()
    selected = data['selected']

    # Удаляем выбранные блюда из users
    remaining = [d for d in users[uid]['custom_dishes'] if d not in selected]
    users[uid]['custom_dishes'] = remaining

    # Очищаем FSM
    await state.clear()

    # Ответ пользователю
    names = [d['name'] for d in selected]
    text = (
        f"Удалено блюд: {len(selected)}\n"
        f"Список удалённых: {', '.join(names)}"
    )
    if (callback.message is not None) and (hasattr(callback.message, 'edit_text')):
        await callback.message.edit_text(text=text, reply_markup=return_select())
    await callback.answer("Удаление завершено")

# Рацион дня

@router.callback_query(F.data == "⌛Рацион на день")
async def show_today(callback: CallbackQuery, state: FSMContext):
    uid = callback.from_user.id

    try: dishes = users[uid]['custom_dishes']

    except KeyError:
        await callback.answer("Пожалуйста, сначала добавьте блюда.")
        return

    if not dishes or len(dishes) == 0:
        await callback.answer("У вас нет добавленных блюд.")
        return

    await state.clear()

    await state.update_data(dishes=dishes, page=0, selected=[])

    kb = make_menu(dishes, page=0, selected=[])
    if (callback.message is not None) and (hasattr(callback.message, 'edit_text')):
        await callback.message.edit_text("Выберите блюдо из списка ниже:", reply_markup=kb)

    await state.set_state(FSMDietState.selecting)


@router.callback_query(lambda c: c.data and c.data.startswith("toggle:") , FSMDietState.selecting)
async def toggle_dish(callback: CallbackQuery, state: FSMContext):
    if callback.data is None:
        await callback.answer("Неверные данные callback")
        return

    data = await state.get_data()
    dishes, sel, page = data.get("dishes"), data.get("selected"), data.get("page")
    _, idx_str, _ = callback.data.split(":")
    idx = int(idx_str)
    dish = dishes[idx] #type: ignore

    if dish in sel: #type: ignore
        sel.remove(dish) #type: ignore
    else:
        sel.append(dish) #type: ignore

    await state.update_data(selected=sel)
    kb = make_menu(dishes, page, sel) #type: ignore
    if (callback.message is not None) and (hasattr(callback.message, 'edit_text')):
        await callback.message.edit_text("Выберите блюдо из списка ниже:", reply_markup=kb)

    await callback.answer()

@router.callback_query(lambda c: c.data and c.data.startswith("page:"), FSMDietState.selecting)
async def change_page(callback: CallbackQuery, state: FSMContext):

    if callback.data is None:
        await callback.answer("Неверные данные callback")
        return

    data = await state.get_data()
    dishes, sel = data['dishes'], data['selected']
    page = int(callback.data.split(":")[1])
    await state.update_data(page=page)
    kb = make_menu(dishes, page, sel)
    if (callback.message is not None) and (hasattr(callback.message, 'edit_text')):
        await callback.message.edit_text("Выберите блюда на сегодня:", reply_markup=kb)
    await callback.answer()

@router.callback_query(F.data == "confirm", FSMDietState.selecting)
async def confirm_selection(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    sel = data['selected']

    total_c = sum(float(d['carbs']) for d in sel)
    total_p = sum(float(d['protein']) for d in sel)
    total_f = sum(float(d['fats']) for d in sel)
    calories = total_c*4 + total_p*4 + total_f*9

    text = (
        f"📋 *Ваш рацион на сегодня:*\n\n"
        f"– Блюд выбрано: {len(sel)}\n"
        f"– Углеводы: {total_c:.0f} грамм\n"
        f"– Белки: {total_p:.0f} грамм\n"
        f"– Жиры: {total_f:.0f} грамм\n"
        f"– Калории: {calories:.0f} ккал"
    )
    if (callback.message is not None) and (hasattr(callback.message, 'edit_text')):
        await callback.message.edit_text(text, parse_mode="Markdown")

    try:
        tdee = float(users[callback.from_user.id]['user_info']["tdee"])
    except KeyError:
        await callback.message.answer(text="Вы не указали свою суточную норму калорий.\nЧтобы её указать, нажмите кнопку Настроить профиль в главном меню.", reply_markup=return_select()) #type: ignore
        return
    if calories > tdee + 200:
        text1 = "Вы превысили свою суточную норму калорий!\n"
    elif calories < tdee - 200:
        text1 = "Вы не достигли своей суточной нормы калорий!\n"
    else:
        text1 = "Вы достигли своей примерной суточной нормы калорий!\n"
    text2 = "Ваша суточная норма калорий: " + str(tdee) + " ккал\n\n"

    tdee_carbs = tdee * 0.45
    tdee_protein = tdee * 0.3
    tdee_fats = tdee * 0.25

    if total_c * 4 > tdee_carbs + 100:
        text3 = "🍞 Углеводы превышены! Постарайтесь сократить хлеб, картофель и сладости в рационе.\n\n"
    elif total_c * 4 < tdee_carbs - 150:
        text3 = "⚡️ Недостаток углеводов! Добавьте в меню больше круп, макарон и цельнозернового хлеба.\n\n"
    else:
        text3 = "✅ Отлично! Вы находитесь в пределах суточной нормы углеводов.\n\n"

    if total_p * 4 > tdee_protein + 250:
        text4 = "🥩 Избыток белка! Уменьшите порции мяса, рыбы и молочных продуктов.\n\n"
    elif total_p * 4 < tdee_protein - 100:
        text4 = "💪 Белка недостаточно! Включите в рацион больше мяса, рыбы, молока или яиц.\n\n"
    else:
        text4 = "👍 Отлично! Вы попадаете в рекомендованную суточную норму белка.\n\n"

    if total_f * 9 > tdee_fats + 100:
        text5 = "🥜 Жиров многовато! Сократите масла, орехи и жирное мясо в своём рационе.\n\n"
    elif total_f * 9 < tdee_fats - 100:
        text5 = "🥑 Жиров не хватает — добавьте орехи, авокадо или растительные масла.\n\n"
    else:
        text5 = "🎉 Прекрасно! Жиры находятся в пределах дневной нормы.\n\n"

    final_text = text1 + text2 + text3 + text4 + text5
    await callback.message.answer(text=final_text, reply_markup=return_select()) #type: ignore

    # очищаем FSM после завершения
    await state.clear()


@router.callback_query(F.data.in_(["dish_no_callback", "🥗Добавить блюда"]))
async def new_dish_callback(callback: CallbackQuery, state: FSMContext):
    if (callback.message is not None) and (hasattr(callback.message, 'edit_text')):
        await callback.message.edit_text('Отправьте количество углеводов (грамм) в вашем блюде.')
        await state.clear()
        await state.set_state(FSMFillDish.dish_carbs)
    else:
        await callback.answer()


@router.callback_query(F.data.in_(["user_no_callback", "👀Настроить профиль"]), user_exists)
async def reuser_callback(callback: CallbackQuery, state: FSMContext):
    if (callback.message is not None) and (hasattr(callback.message, 'edit_text')):
        await callback.message.edit_text('Вы решили указать информацию о себе\nДля начала введите свой возраст.')
        await state.clear()
        await state.set_state(FSMFillUser.user_age)

    else:
        await callback.answer()


@router.callback_query(F.data == "dish_yes_callback", StateFilter(FSMFillDish.end), user_exists)
async def dish_menu_callback(callback: CallbackQuery, state: FSMContext):
    if (callback.message is not None) and (hasattr(callback.message, 'edit_text')):

        user_id = callback.from_user.id

        data = await state.get_data()
        dish_data = cast(DishData, data)

        # Если пользователь нажал Подтвердить создание блюда, сохраняем
        users[user_id]['custom_dishes'].append(dish_data)

        await state.clear()

        logging.info(users[callback.from_user.id])
        await callback.message.edit_text('Это меню. Здесь вы можете выбрать, что хотите сделать.\nВыберите один из пунктов ниже:', reply_markup=start_menu())

    await callback.answer("Блюдо успешно добавлено!")

@router.callback_query(F.data == "user_yes_callback", StateFilter(FSMFillUser.end), user_exists)
async def user_menu_callback(callback: CallbackQuery, state: FSMContext):
    if (callback.message is not None) and (hasattr(callback.message, 'edit_text')):

        user_id = callback.from_user.id

        user_data = await state.get_data()
        info_data = cast(UserInfoData, user_data)

        # Если пользователь нажал Подтвердить пользователя, сохраняем
        users[user_id]['user_info'] = info_data

        new_age = user_data.get('age', "Не указано")
        new_weight = user_data.get('weight', "Не указано")
        new_height = user_data.get('height', "Не указано")
        new_gender = user_data.get('gender', "Не указано")
        new_activity = user_data.get('activity', "Не указано")

        await add_user_info(user_id, new_age, new_weight, new_height, new_gender, new_activity)

        await state.clear()

        logging.info(users[callback.from_user.id])
        await callback.message.edit_text('Это меню. Здесь вы можете выбрать, что хотите сделать.\nВыберите один из пунктов ниже:', reply_markup=start_menu())

    await callback.answer("Данные пользователя успешно обновлены!")