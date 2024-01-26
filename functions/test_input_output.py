import os

from aiogram import Router, F
from bot import bot

from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.builders import generator
from keyboards.reply import rmk, main_tch, main_st

from data.database import DataBase

from utils.validity import vl_exl
from utils.generator_id import test_name
from utils.states import Test_inp, Perform_test
from utils.question_answer import question_answer

router = Router()

@router.message(F.text == "Отмена❌")
async def create_test(message: Message, state: FSMContext):
    await state.clear()
    fl = await DataBase.check(["tg_id", "role"], message.chat.id)

    await message.answer(
        "Главное меню:",
        reply_markup=(main_tch if fl[0][1] in ['Учитель'] else main_st))

@router.message(F.text.lower() == "создать тест📗")
async def create_test(message: Message, state: FSMContext):
    fl = await DataBase.check(["tg_id", "role"], message.chat.id)

    if len(fl) > 0 and [True if fl[0][1] in ['Учитель'] else False][0]:
        await state.set_state(Test_inp.num_class)
        await message.answer("Для какого класса вы хотите создать тест?",
                            reply_markup=generator([str(i) for i in range(1, 12)]))
    elif len(fl) == 0:
        await message.answer("Сначала зарегистрируйтесь!", reply_markup=rmk)
        await message.answer("/start")
    else:
        await message.answer("Вы не учитель!",
                            reply_markup=main_st)


@router.message(Test_inp.num_class, F.text)
async def num_class(message: Message, state: FSMContext):
    if message.text in [str(i) for i in range(1, 12)]:
        await state.update_data(id_teacher=message.chat.id)
        await state.update_data(num_class=message.text)
        await state.set_state(Test_inp.name_test)
        await message.answer("Как называется ваш тест?",
                             reply_markup=rmk)
    else:
        await message.answer("Введите номер класса от 1 до 11")

@router.message(Test_inp.num_class, ~F.text)
async def inc_num_class(message: Message, state: FSMContext):
    await message.answer("Введите номер класса от 1 до 11")


@router.message(Test_inp.name_test, F.text)
async def test_names(message: Message, state: FSMContext):
    await state.update_data(test_name=message.text)
    await state.set_state(Test_inp.id_test)
    await message.answer("Хорошо, а теперь отправьте мне файл с расширением .xlsx, в колонке А которого находятся вопросы, а в колонке В ответы к этим вопросам")

@router.message(Test_inp.name_test, ~F.text)
async def inc_test_names(message: Message, state: FSMContext):
    await message.answer("Введите название теста!")


@router.message(Test_inp.id_test, F.document)
async def download(message: Message, state: FSMContext):
    if message.document.mime_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        file = await bot.get_file(message.document.file_id)
        file_path = file.file_path
        name = test_name()

        await bot.download_file(file_path, "data/tests/" + name + ".xlsx")
        vlexcel = await vl_exl(name)
        if vlexcel[0]:
            await state.update_data(id_test=name)
            await state.update_data(quantity=vlexcel[1])

            data_zxc = await state.get_data()
            await state.clear()

            await DataBase.insert_test(list(data_zxc.values()))
            await message.answer("Тест создан! Теперь вы можете отправить этот код мероприятия своим ученикам, чтобы они могли начать проходить тестирование:")
            await message.answer(name, reply_markup=main_tch)
        else:
            await message.answer("Файл не соответствует шаблону!",
                                 reply_markup=generator("Отмена❌"))
            os.remove("data/tests/" + name + ".xlsx")
    else:
        await message.answer("Выберите файл с расширением .xlsx!",
                             reply_markup=generator("Отмена❌"))

@router.message(Test_inp.id_test, ~F.document)
async def inc_download(message: Message, state: FSMContext):
    await message.answer("Выберите файл с расширением .xlsx!",
                         reply_markup=generator("Отмена❌"))


@router.message(F.text.lower() == "пройти тест🗒️")
async def test_inp(message: Message, state: FSMContext):
    fl = await DataBase.check(["tg_id", "role"], message.chat.id)

    if len(fl) > 0 and [True if fl[0][1] in ['Ученик'] else False][0]:
        await message.answer("Введите id теста который вам дал учитель:", reply_markup=rmk)
        await state.set_state(Perform_test.valid_test)
    elif len(fl) == 0:
        await message.answer("Сначала зарегистрируйтесь!", reply_markup=rmk)
        await message.answer("/start")
    else:
        await message.answer("Ты не ученик!",
                            reply_markup=main_tch)


@router.message(Perform_test.valid_test, F.text)
async def valid_test(message: Message, state: FSMContext):
    id = message.text
    fl = await DataBase.check(["id_test", "name_test", "id_teacher", "quantity_test"], id, table="test")

    if len(fl) > 0:
        th_name = await DataBase.check(["tg_id", "name"], fl[0][-2])
        await message.answer(f"Это тест от {th_name[0][-1]} на тему \"{fl[0][1]}\", в нём {fl[0][-1]} вопросов")
        await message.answer("Начать выполнение теста?",
                             reply_markup=generator(["Начать", "Отмена"]))

        await state.update_data(id_stud=message.chat.id)
        await state.update_data(name_test=id)
        await state.update_data(name_test_text=fl[0][1])
        await state.update_data(id_teacher=fl[0][2])
        await state.update_data(max_test=fl[0][-1])
        await state.update_data(test_num=0)
        await state.update_data(count=0)

        await state.set_state(Perform_test.start_test)
    else:
        await message.answer("Такого теста не существует, попробуйте ввести внимательней",
                             reply_markup=generator("Отмена❌"))

@router.message(Perform_test.valid_test, ~F.text)
async def inc_valid_test(message: Message, state: FSMContext):
    await message.answer("Введите пяти-символьный код мероприятия который тебе дал учитель!",
                         reply_markup=generator("Отмена❌"))


@router.message(Perform_test.start_test, F.text.lower().in_(["начать"]))
async def start_test(message: Message, state: FSMContext):
    global question, answer

    temp_data = await state.get_data()
    question, answer = await question_answer(temp_data['name_test'])

    await message.answer(f"{temp_data['test_num']+1}. {question[temp_data['test_num']]}",
                         reply_markup=rmk)
    await state.set_state(Perform_test.state_test1)

@router.message(Perform_test.start_test, F.text.lower().in_(["отмена"]))
async def start_test(message: Message, state: FSMContext):
    await message.answer("Прохождение теста отменено",
                         reply_markup=main_st)
    await state.clear()

@router.message(Perform_test.start_test, ~F.text)
async def inc_start_test(message: Message, state: FSMContext):
    await message.answer("Нажмите на кнопку ниже",
                         reply_markup=generator(["Начать", "Отмена"]))

@router.message(Perform_test.state_test1)
async def start_test(message: Message, state: FSMContext):
    temp_data = await state.get_data()

    if message.text.lower() == str(answer[temp_data['test_num']]).lower():
        await state.update_data(count=temp_data['count']+1)

    if temp_data['test_num']+1 < temp_data['max_test']:
        await state.update_data(test_num=temp_data['test_num'] + 1)

        temp_data = await state.get_data()
        await message.answer(f"{temp_data['test_num'] + 1}. {question[temp_data['test_num']]}")
        await state.set_state(Perform_test.state_test2)
    else:
        temp_data = await state.get_data()

        grade = round((temp_data['count']/temp_data['max_test'])*5)
        await message.answer(f"Конец, вы выполнили тест на {temp_data['count']} из {temp_data['max_test']}")
        await message.answer(f"Ваша примерная оценка - {grade if grade > 2 else 2}",
                             reply_markup=main_st)

        name_st = await DataBase.check(["tg_id", "name"], message.chat.id)
        await DataBase.result_test(list(temp_data.values())[0:3] + [grade if grade > 2 else 2] + [name_st[0][1]])

        zxc = await DataBase.check(["tg_id", "name", "ch_class"], temp_data['id_stud'])
        await bot.send_message(temp_data['id_teacher'],
                               f"{zxc[0][1]}, ученик {zxc[0][2]} класса прошел ваш тест на {grade if grade > 2 else 2}")

        await state.clear()


@router.message(Perform_test.state_test2)
async def start_test(message: Message, state: FSMContext):
    temp_data = await state.get_data()

    if message.text.lower() == str(answer[temp_data['test_num']]).lower():
        await state.update_data(count=temp_data['count']+1)

    if temp_data['test_num']+1 < temp_data['max_test']:
        await state.update_data(test_num=temp_data['test_num'] + 1)

        temp_data = await state.get_data()
        await message.answer(f"{temp_data['test_num'] + 1}. {question[temp_data['test_num']]}")
        await state.set_state(Perform_test.state_test1)
    else:
        temp_data = await state.get_data()

        grade = round((temp_data['count'] / temp_data['max_test']) * 5)
        await message.answer(f"Конец, вы выполнили тест на {temp_data['count']} из {temp_data['max_test']}")
        await message.answer(f"Ваша примерная оценка - {grade if grade > 2 else 2}",
                             reply_markup=main_st)

        name_st = await DataBase.check(["tg_id", "name"], message.chat.id)
        await DataBase.result_test(list(temp_data.values())[0:3] + [grade if grade > 2 else 2] + [name_st[0][1]])

        zxc = await DataBase.check(["tg_id", "name", "ch_class"], temp_data['id_stud'])
        await bot.send_message(temp_data['id_teacher'],
                               f"{zxc[0][1]}, ученик {zxc[0][2]} класса прошел ваш тест на {grade if grade > 2 else 2}")

        await state.clear()