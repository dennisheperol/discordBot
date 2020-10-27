from typing import List

from domain.poop_balance import PoopBalance
from infrastructure.helpers import wrapper


class PoopBalanceRepo:

    def set_poop_balance(self, poop_balance: PoopBalance):
        wrapper(self._set_poop_balance_func, poop_balance)

    def get_poop_balance(self, discord_id) -> PoopBalance:
        return wrapper(self._get_poop_balance_func, discord_id)

    def get_highest_balances(self, amount) -> List[PoopBalance]:
        return wrapper(self._get_highest_balances_func, amount)

    @staticmethod
    def _set_poop_balance_func(db, poop_balance: PoopBalance):
        sql_update_query = """INSERT INTO poop_balance (id, balance) VALUES (%(id)s,%(balance)s)
        ON CONFLICT (id) DO
        UPDATE SET balance = %(balance)s"""
        db['cursor'].execute(sql_update_query, {'id': poop_balance.id, 'balance': poop_balance.balance})
        db['connection'].commit()

    @staticmethod
    def _get_poop_balance_func(db, discord_id) -> PoopBalance:
        sql_select_query = """SELECT * FROM poop_balance WHERE id = %(id)s"""
        db['cursor'].execute(sql_select_query, {'id': discord_id})
        rows = db['cursor'].fetchall()
        if len(rows) > 0:
            return PoopBalance(rows[0])
        else:
            return PoopBalance((discord_id, 0))

    @staticmethod
    def _get_highest_balances_func(db, limit) -> List[PoopBalance]:
        sql_select_query = """SELECT * FROM poop_balance ORDER BY balance DESC LIMIT %(limit)s"""
        db['cursor'].execute(sql_select_query, {'limit': limit})
        rows = db['cursor'].fetchall()
        return list(map(lambda row: PoopBalance(row), rows))


poop_balance_repo = PoopBalanceRepo()
