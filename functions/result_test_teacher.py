from aiogram import Router, F

from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.builders import generator
from keyboards.reply import rmk, main_tch, main_st

from data.database import DataBase

from utils.states import Result_test

router = Router()

@router.message(F.text == "Отмена❌")
async def create_test(message: Message, state: FSMContext):
    await state.clear()
    fl = await DataBase.check(["tg_id", "role"], message.chat.id)

    await message.answer(
        "Главное меню:",
        reply_markup=main_tch)

@router.message(F.text.lower() == "результаты тестов📘")
async def result_test(message: Message, state: FSMContext):
    fl = await DataBase.check(["tg_id", "role"], message.chat.id)

    if len(fl) > 0 and [True if fl[0][1] in ['Учитель'] else False][0]:
        await state.set_state(Result_test.check_t)
        await message.answer("Введите код мероприятия",
                            reply_markup=rmk)
    elif len(fl) == 0:
        await message.answer("Сначала зарегистрируйтесь!", reply_markup=rmk)
        await message.answer("/start")
    else:
        await message.answer("Вы не учитель!",
                            reply_markup=main_st)

@router.message(Result_test.check_t, F.text)
async def chek_t(message: Message, state: FSMContext):
    id = message.text
    if len(id) == 5:
        fl = await DataBase.check(["id_test", "id_teacher"], id, table="test")

        if len(fl) > 0 and fl[0][1] == message.chat.id:
            fl = await DataBase.check(["id_test", "name_test", "name_student", "grade"], id, table="result_test")

            if len(fl) > 0:
                await message.answer(f'Результаты теста "{fl[0][1]}":\n' + '\n'.join([f"{i[2]} - {i[-1]}" for i in fl]),
                                     reply_markup=main_tch)
                await state.clear()
            else:
                await message.answer("Ваш тест еще никто не проходил",
                                     reply_markup=main_tch)
                await state.clear()

        elif len(fl) > 0:
            await message.answer("Это не ваш тест!",
                                 reply_markup=main_tch)
            await state.clear()
        else:
            await message.answer("Неверный код мероприятия, попробуйте еще раз",
                                 reply_markup=generator("Отмена❌"))
    else:
        await message.answer("Неверный код мероприятия, попробуйте еще раз",
                             reply_markup=generator("Отмена❌"))

@router.message(Result_test.check_t, ~F.text)
async def inc_chek_t(message: Message, state: FSMContext):
    await message.answer("Неверный код мероприятия, попробуйте еще раз",
                         reply_markup=generator("Отмена❌"))
