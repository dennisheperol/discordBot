from infrastructure.helpers import wrapper


def set_scavenge_time(discord_id, time):
    wrapper(set_scavenge_time_func, {'discord_id': discord_id, 'time': time})


def get_scavenge_time(discord_id):
    return wrapper(get_scavenge_time_func, {'discord_id': discord_id})


def set_scavenge_time_func(db, args):
    sql_update_query = """INSERT INTO scavenge_time (id, time) VALUES (%(id)s,%(time)s)
    ON CONFLICT (id) DO
    UPDATE SET time = %(time)s"""
    db['cursor'].execute(sql_update_query, {'id': args['discord_id'], 'time': args['time']})
    db['connection'].commit()


def get_scavenge_time_func(db, args):
    sql_select_query = """SELECT time FROM scavenge_time WHERE id = %(id)s"""
    db['cursor'].execute(sql_select_query, {'id': args['discord_id']})
    rows = db['cursor'].fetchall()
    if len(rows) > 0:
        return rows[0][0]
    else:
        return 0
