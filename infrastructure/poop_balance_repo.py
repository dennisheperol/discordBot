from infrastructure.helpers import wrapper


def increase_poop_balance(discord_id, increment):
    wrapper(increase_poop_balance_func, {'discord_id': discord_id, 'increment': increment})


def get_poop_balance(discord_id):
    return wrapper(get_poop_balance_func, {'discord_id': discord_id})


def increase_poop_balance_func(db, args):
    sql_update_query = """INSERT INTO poop_balance (id, balance) VALUES (%(id)s,%(increment)s)
    ON CONFLICT (id) DO
    UPDATE SET balance = poop_balance.balance + %(increment)s"""
    db['cursor'].execute(sql_update_query, {'id': args['discord_id'], 'increment': args['increment']})
    db['connection'].commit()


def get_poop_balance_func(db, args):
    sql_select_query = """SELECT balance FROM poop_balance WHERE id = %(id)s"""
    db['cursor'].execute(sql_select_query, {'id': args['discord_id']})
    rows = db['cursor'].fetchall()
    if len(rows) > 0:
        return rows[0][0]
    else:
        return 0
