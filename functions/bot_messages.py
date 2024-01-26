from aiogram import Router, F
from aiogram.types import Message

from keyboards.reply import main_tch, main_st, rmk
from data.database import DataBase

router = Router()


@router.message(F.text == "Назад↩️")
async def back(message: Message):
    fl = await DataBase.check(["tg_id", "role"], message.chat.id)

    await message.answer(
        'Главное меню:',
        reply_markup=(main_tch if fl[0][1] in ['Учитель'] else main_st))


@router.message()
async def echo(message: Message):
    fl = await DataBase.check(["tg_id", "role"], message.chat.id)

    if len(fl) > 0:
        await message.answer('Главное меню:',
                             reply_markup=(main_tch if fl[0][1] in ['Учитель'] else main_st))
    else:
        await message.answer("Сначала зарегистрируйтесь!", reply_markup=rmk)
        await message.answer("/start")