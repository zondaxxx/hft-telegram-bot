from aiogram import Router, F

from aiogram.types import Message
from keyboards.reply import rmk, main_tch, main_st

from data.database import DataBase

router = Router()

@router.message(F.text.lower() == "мои тесты📕")
async def my_tests(message: Message):
    fl = await DataBase.check(["tg_id", "role"], message.chat.id)

    if len(fl) > 0 and [True if fl[0][1] in ["Учитель"] else False][0]:
        fl = await DataBase.check(["id_teacher", "name_test", "num_class", "quantity_test", "id_test"], message.chat.id, table="test")
        if len(fl) > 0:
            await message.answer("\n\n".join([f'"{i[1]}" - тест для {i[2]} класса на {i[3]} вопросов, код: {i[-1]}' for i in fl]),
                                reply_markup=main_tch)
        else:
            await message.answer("У вас пока нет тестов",
                                 reply_markup=main_tch)
    elif len(fl) == 0:
        await message.answer("Сначала зарегистрируйтесь!", reply_markup=rmk)
        await message.answer("/start")
    else:
        await message.answer("Вы не учитель!",
                            reply_markup=main_st)


@router.message(F.text.lower() == "мои отметки📈")
async def my_tests(message: Message):
    fl = await DataBase.check(["tg_id", "role"], message.chat.id)

    if len(fl) > 0 and [True if fl[0][1] in ["Ученик"] else False][0]:
        fl = await DataBase.check(["id_student", "name_test", "grade", "id_test"], message.chat.id, table="result_test")
        if len(fl) > 0:
            await message.answer("\n\n".join([f'"{i[1]}" - ваша отметка за этот тест {i[2]} (ID: {i[-1]})' for i in fl]),
                                reply_markup=main_st)
        else:
            await message.answer("У вас пока нет отметок",
                                 reply_markup=main_st)
    elif len(fl) == 0:
        await message.answer("Сначала зарегистрируйтесь!", reply_markup=rmk)
        await message.answer("/start")
    else:
        await message.answer("Вы не ученик!",
                            reply_markup=main_tch)