from typing import List

from domain.poop_balance import PoopBalance
from infrastructure.helpers import wrapper


def set_poop_balance(poop_balance: PoopBalance):
    wrapper(set_poop_balance_func, poop_balance)


def get_poop_balance(discord_id) -> PoopBalance:
    return wrapper(get_poop_balance_func, discord_id)


def get_top_balances(amount=10):
    return wrapper(get_top_balances_func, amount)


def set_poop_balance_func(db, poop_balance: PoopBalance):
    sql_update_query = """INSERT INTO poop_balance (id, balance) VALUES (%(id)s,%(balance)s)
    ON CONFLICT (id) DO
    UPDATE SET balance = %(balance)s"""
    db['cursor'].execute(sql_update_query, {'id': poop_balance.id, 'balance': poop_balance.balance})
    db['connection'].commit()


def get_poop_balance_func(db, discord_id) -> PoopBalance:
    sql_select_query = """SELECT * FROM poop_balance WHERE id = %(id)s"""
    db['cursor'].execute(sql_select_query, {'id': discord_id})
    rows = db['cursor'].fetchall()
    if len(rows) > 0:
        return PoopBalance(rows[0])
    else:
        return PoopBalance((discord_id, 0))


def get_top_balances_func(db, limit) -> List[PoopBalance]:
    sql_select_query = """SELECT * FROM poop_balance ORDER BY balance DESC LIMIT %(limit)s"""
    db['cursor'].execute(sql_select_query, {'limit': limit})
    rows = db['cursor'].fetchall()
    return list(map(lambda row: PoopBalance(row), rows))
