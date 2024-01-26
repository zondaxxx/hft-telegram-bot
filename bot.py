import asyncio
from aiogram import Bot, Dispatcher

from data.database import DataBase
from functions import bot_messages, user_commands, start_reg, test_input_output, my_test_grade, result_test_teacher

from config_reader import config

bot = Bot(config.bot_token.get_secret_value() , parse_mode="HTML")

async def main(bot):
    dp = Dispatcher()
    db = DataBase("users_db.db")

    await db.create_table()
    dp.include_routers(
        user_commands.router,
        start_reg.router,
        test_input_output.router,
        my_test_grade.router,
        result_test_teacher.router,
        bot_messages.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main(bot))
