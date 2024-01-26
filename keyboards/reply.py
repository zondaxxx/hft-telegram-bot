from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove
)

main_tch = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Создать тест📗"),
            KeyboardButton(text="Мои тесты📕"),
            KeyboardButton(text="Результаты тестов📘")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder="Выберите действие из меню...",
    selective=True
)

main_st = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Пройти тест🗒️"),
            KeyboardButton(text="Мои отметки📈")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder="Выберите действие из меню...",
    selective=True
)

rmk = ReplyKeyboardRemove()

