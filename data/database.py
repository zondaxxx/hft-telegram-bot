import aiosqlite

class DataBase:
    def __init__(self, name: str) -> None:
        self.name = f"data/{name}"

    async def create_table(self):
        async with aiosqlite.connect(self.name) as db:
            sql = await db.cursor()

            list1 = f"""CREATE TABLE IF NOT EXISTS users (
                tg_id INT,
                name VARCHAR(30),
                role VARCHAR(7),
                ch_class TINYINT,
                subject VARCHAR(50))"""

            list2 = f"""CREATE TABLE IF NOT EXISTS test (
                id_teacher INT,
                num_class TINYINT,
                name_test TEXT,
                id_test VARCHAR(5),
                quantity_test TINYINT)"""

            list3 = f"""CREATE TABLE IF NOT EXISTS result_test (
                id_student INT,
                id_test VARCHAR(5),
                name_test TEXT,
                grade TININT,
                name_student TEXT)"""

            for qr in [list1, list2, list3]:
                await sql.executescript(qr)
                await db.commit()

    async def insert_reg(data_zxc: list) -> None:
        async with aiosqlite.connect("data/users_db.db") as db:
            sql = await db.cursor()

            if data_zxc[2].lower() == "ученик":
                await sql.execute("""INSERT INTO users (
                    tg_id,
                    name,
                    role,
                    ch_class) 
                    VALUES (?, ?, ?, ?)""",
                    data_zxc)
            else:
                await sql.execute("""INSERT INTO users (
                    tg_id,
                    name,
                    role,
                    subject) 
                    VALUES (?, ?, ?, ?)""",
                    data_zxc)
            await db.commit()

    async def insert_test(data_zxc: list) -> None:
        async with aiosqlite.connect("data/users_db.db") as db:
            sql = await db.cursor()

            await sql.execute("""INSERT INTO test (
            id_teacher,
            num_class,
            name_test,
            id_test,
            quantity_test)
            VALUES (?, ?, ?, ?, ?)""",
            data_zxc)

            await db.commit()

    async def insert_test(data_zxc: list) -> None:
        async with aiosqlite.connect("data/users_db.db") as db:
            sql = await db.cursor()

            await sql.execute("""INSERT INTO test (
            id_teacher,
            num_class,
            name_test,
            id_test,
            quantity_test)
            VALUES (?, ?, ?, ?, ?)""",
            data_zxc)

            await db.commit()


    async def result_test(data_zxc: list) -> None:
        async with aiosqlite.connect("data/users_db.db") as db:
            sql = await db.cursor()

            await sql.execute("""INSERT INTO result_test (
            id_student,
            id_test,
            name_test,
            grade,
            name_student)
            VALUES (?, ?, ?, ?, ?)""",
            data_zxc)

            await db.commit()

    async def check(col: list, row: str, table = 'users',  flag: bool = True):
        async with aiosqlite.connect("data/users_db.db") as db:
            sql = await db.cursor()

            if flag:
                abc = await sql.execute(f"SELECT {', '.join(col)} FROM {table} WHERE {col[0]} = '{row}' ")
                return await sql.fetchall()
            else:
                pass