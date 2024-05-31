import re

import asyncpg
from datetime import datetime
class Libowsky(Exception):
    pass

class EventManager:
    settings = {
        "user": 'postgres',
        "password": '123',
        "database": 'telebot',
        "host": 'localhost',
        "port": 5432,
    }

    async def set_credit(
            self,
            bank_name: str,
            credit_percent: int,
            start_date: str,
            end_date: str,
            credit_balance: int,
            score_name: str,
            user_id: int
    ):
        conn = await asyncpg.connect(**self.settings)

        query = (
            '''INSERT INTO credit 
                (bank_name, credit_percent, start_date, end_date, sum, score_id) 
                VALUES ($1, $2, $3, $4, $5, (SELECT id FROM score WHERE name = $6 AND user_tg = $7))'''
        )

        set_balance = (
            '''UPDATE score SET sum = sum + $1 
                WHERE id = (SELECT id FROM score WHERE name = $2 AND user_tg = $3)'''
        )

        await conn.fetchval(
            set_balance,
            int(credit_balance),
            score_name,
            int(user_id),
        )

        result = await conn.fetchval(
            query,
            bank_name,
            int(credit_percent),
            datetime.strptime(start_date, '%Y-%m-%d'),
            datetime.strptime(end_date, '%Y-%m-%d'),
            int(credit_balance),
            score_name,
            int(user_id)
        )

        await conn.close()

        return result

    async def get_credits(
            self,
            user_id: int
    ):

        conn = await asyncpg.connect(**self.settings)

        query = 'SELECT c.bank_name, c.sum, s.name FROM credit c JOIN score s ON c.score_id = s.id where s.user_tg = $1'

        result = await conn.fetch(query, user_id)
        await conn.close()
        result_list = []
        for item in result:
            data = []
            data.append(item["bank_name"])
            data.append(item["sum"])
            data.append(item["name"])
            result_list.append(data)


        return result_list
    async def del_credit(
            self,
            credit_name: str,
            user_id: int,
    ):
        conn = await asyncpg.connect(**self.settings)

        query = f"DELETE FROM credit WHERE score_id IN (SELECT id FROM score WHERE bank_name = $1 AND user_tg = $2)"

        await conn.fetchval(
            query,
            credit_name,
            user_id
        )

    async def view_all_income(self, user_id: int):
        conn = await asyncpg.connect(**self.settings)

        query = f"SELECT income.sum FROM income join score on income.score_id = score.id WHERE score.user_tg = {user_id}"

        result = await conn.fetchval(query)

        await conn.close()

        return result

    async def add_new_income(
            self,
            income_name: str,
            income_sum: str,
            income_category_name: str,
            income_score_name: str,
            user_id: int
    ):
        conn = await asyncpg.connect(**self.settings)

        q1 = 'select sum from score where name = $1 and user_tg = $2'

        balance = await conn.fetchval(q1, income_score_name, user_id)

        if int(balance) - int(income_sum) > 0:

            minus_money = 'update score set sum = $1 where name = $2 and user_tg = $3'

            await conn.fetchval(minus_money, int(balance) - int(income_sum), income_score_name, user_id)

            query = ("INSERT INTO income (name, timestamp, sum, category_id, score_id)"
                     " VALUES ($1, now(), $2, (select id from income_category where name = $3),"
                     "(select id from score where name = $4 and user_tg = $5))")

            result = await conn.fetchval(
                query,
                income_name,
                int(income_sum),
                income_category_name,
                income_score_name,
                user_id
            )
        else:
            raise Libowsky("Недостаточно средств на счету.")

        await conn.close()

        return result

    async def delete_income(self, income_name: str, user_id: int):

        conn = await asyncpg.connect(**self.settings)

        q1 = 'update score set sum = (score.sum + income.sum) from income where income.name = $1 and score.id = income.score_id and user_tg = $2'

        await conn.fetchval(q1, income_name, user_id)
        await conn.close()


    async def add_income_category(self, income_name_cat: str):
        conn = await asyncpg.connect(**self.settings)

        q1 = 'insert into income_category (name) values ($1)'

        await conn.fetchval(q1, income_name_cat)
        await conn.close()


    async def del_income_category(self, income_name_cat: str):
        conn = await asyncpg.connect(**self.settings)

        q1 = 'delete from income_category where name = $1'

        await conn.fetchval(q1, income_name_cat)
        await conn.close()

    async def get_income_category(self, user_id: int):

        conn = await asyncpg.connect(**self.settings)

        q1 = ('select income_category.name from income_category '
              'join income on income.category_id = income_category.id '
              'join score on score.id = income.score_id where score.user_tg = $1 group by income_category.name')

        result = await conn.fetch(q1, user_id)
        await conn.close()
        res_list = []

        for item in result:
            res_list.append(item['name'])

        return re.match(r'\[(.+)\]', str(res_list)).group(1)


    async def get_incomes(self, user_id: int):
        conn = await asyncpg.connect(**self.settings)

        q1 = 'select income.name from income join score on score.id = income.score_id where score.user_tg = $1'

        result = await conn.fetch(q1, user_id)
        await conn.close()
        res_list = []

        for item in result:
            res_list.append(item['name'])

        return [re.match('(\b\w+\b)', r ) for r in res_list]  # noqa

    async def insert_new_score(
            self,
            user_id: int,
            name: str,
            summ: int
    ):
        try:
            conn = await asyncpg.connect(**self.settings)

            query = "INSERT INTO score (name, sum, user_tg) VALUES ($1, $2, $3)"

            result = await conn.fetchval(query, name, int(summ), user_id)

            await conn.close()

            return result

        except Exception as e:
            raise Exception from e

    async def get_user_score(self, user_id: int):

        conn = await asyncpg.connect(**self.settings)

        query = "select score.name, score.sum from score where user_tg = $1"
        result = await conn.fetch(query, user_id)

        await conn.close()

        res_list = []

        for item in result:
            res_list.append(item['name'])

        return re.match(r'\[(.+)\]', str(res_list)).group(1) # noqa

    async def del_user_score(self, user_id: int, score_name: str):

        conn = await asyncpg.connect(**self.settings)

        query = "delete from score where user_tg = $1 and name = $2"
        result = await conn.fetch(query, user_id, score_name)

        await conn.close()

        return result
