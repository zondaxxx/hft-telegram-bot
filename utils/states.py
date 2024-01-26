from aiogram.fsm.state import StatesGroup, State

class Form(StatesGroup):
    tg_id = State()
    name = State()
    role = State()
    ch_class = State()
    subject = State()

class Test_inp(StatesGroup):
    name_test = State()
    num_class = State()
    id_test = State()
    id_teacher = State()
    quantity_tests = State()

class Perform_test(StatesGroup):
    valid_test = State()
    start_test = State()
    state_test1 = State()
    state_test2 = State()

class Result_test(StatesGroup):
    check_t = State()

