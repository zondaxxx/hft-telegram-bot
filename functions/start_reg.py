from aiogram import Router, F

from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from utils.states import Form
from keyboards.builders import generator
from keyboards.reply import rmk, main_tch, main_st
from data.database import DataBase
from utils.validity import fio, klass

router = Router()


@router.message(CommandStart())
async def register(message: Message, state: FSMContext):
    fl = await DataBase.check(["tg_id", "role"], message.chat.id)

    if len(fl) == 0:
        await state.set_state(Form.name)
        await message.answer("Привет, меня зовут QuizBot, я буду устраивать тесты для проверки твоих знаний и передавать результаты твоему учителю, так что давай дружить ;)")
        await message.answer("Пред началом использования бота вам нужно пройти регистрацию")
        await message.answer("Введите свою ФИО (пример: Иванов И.И.):")
    else:
        await message.answer(
            "Вы уже зарегестрированы!",
            reply_markup=(main_tch if fl[0][1] in ['Учитель'] else main_st))


@router.message(Form.name, F.text)
async def form_name(message: Message, state: FSMContext):
    if await fio(message.text):
        await state.update_data(tg_id=message.chat.id)
        await state.update_data(name=message.text)
        await state.set_state(Form.role)
        await message.answer(
            "Приятно познакомиться, а теперь выберите свою роль в школе:",
            reply_markup=generator(["Ученик", "Учитель"]))
    else:
        await message.answer('Введите своё имя в формате "Фамилия И.О."')

@router.message(Form.name, ~F.text)
async def inc_form_name(message: Message, state: FSMContext):
    await message.answer('Введите своё имя в формате "Фамилия И.О."')


@router.message(Form.role, F.text.in_(["Ученик", "Учитель"]))
async def form_role(message: Message, state: FSMContext):
    await state.update_data(role=message.text)
    if message.text in ["Ученик"]:
        await state.set_state(Form.ch_class)
        await message.answer("В каком классе вы учитесь?",
                             reply_markup=generator([str(i) for i in range(1, 12)]))
    else:
        await state.set_state(Form.subject)
        await message.answer("Учителем какого предмета вы являетесь?", reply_markup=rmk)

@router.message(Form.role)
async def inc_form_role(message: Message, state: FSMContext):
    await message.answer("Нажмите на кнопку",
                         reply_markup=generator(["Ученик", "Учитель"]))


@router.message(Form.ch_class, F.text)
async def form_ch_class(message: Message, state: FSMContext):
    if await klass(message.text):
        await state.update_data(ch_class=message.text)

        data_zxc = await state.get_data()
        await state.clear()

        await DataBase.insert_reg(list(data_zxc.values()))
        await message.answer(
            "Спасибо за регистрацию, теперь вам доступен весь функционал бота!",
            reply_markup=main_st)
    else:
        await message.answer("Выберите свой класс",
                             reply_markup=generator([str(i) for i in range(1, 12)]))

@router.message(Form.ch_class, ~F.text)
async def inc_form_ch_class(message: Message, state: FSMContext):
    await message.answer("Выберите свой класс",
                         reply_markup=generator([str(i) for i in range(1, 12)]))


@router.message(Form.subject)
async def form_subject(message: Message, state: FSMContext):
    await state.update_data(subject=message.text)
    data_zxc = await state.get_data()
    await state.clear()

    await DataBase.insert_reg(list(data_zxc.values()))
    await message.answer(
        "Спасибо за регистрацию, теперь вам доступен весь функционал бота!",
        reply_markup=main_tch)