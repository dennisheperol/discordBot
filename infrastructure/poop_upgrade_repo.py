from infrastructure.helpers import wrapper


def get_poop_upgrade(discord_id):
    return wrapper(get_poop_upgrade_func, {'discord_id': discord_id})


def increase_poop_chance(discord_id, increment=1):
    wrapper(increase_poop_chance_func, {'discord_id': discord_id, 'increment': increment})


def increase_poop_chance_func(db, args):
    sql_update_query = """INSERT INTO poop_upgrade (id, chance) VALUES (%(id)s, %(increment)s)
    ON CONFLICT (id) DO
    UPDATE SET chance = poop_upgrade.chance + %(increment)s"""
    db['cursor'].execute(sql_update_query, {'id': args['discord_id'], 'increment': args['increment']})
    db['connection'].commit()


def get_poop_upgrade_func(db, args):
    sql_select_query = """SELECT chance FROM poop_upgrade WHERE id = %(id)s"""
    db['cursor'].execute(sql_select_query, {'id': args['discord_id']})
    rows = db['cursor'].fetchall()
    if len(rows) > 0:
        return {'chance': rows[0][0]}
    else:
        return {'chance': 0}
