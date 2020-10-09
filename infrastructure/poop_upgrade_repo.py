from domain.poop_upgrade import PoopUpgrade
from infrastructure.helpers import wrapper


def get_poop_upgrade(discord_id) -> PoopUpgrade:
    return wrapper(get_poop_upgrade_func, discord_id)


def set_poop_upgrade(poop_upgrade: PoopUpgrade):
    wrapper(set_poop_upgrade_func, poop_upgrade)


def set_poop_upgrade_func(db, poop_upgrade: PoopUpgrade):
    sql_update_query = """INSERT INTO poop_upgrade (id, chance) VALUES (%(id)s, %(chance)s)
    ON CONFLICT (id) DO
    UPDATE SET chance = %(chance)s"""
    db['cursor'].execute(sql_update_query, {'id': poop_upgrade.id, 'chance': poop_upgrade.chance})
    db['connection'].commit()


def get_poop_upgrade_func(db, discord_id) -> PoopUpgrade:
    sql_select_query = """SELECT * FROM poop_upgrade WHERE id = %(id)s"""
    db['cursor'].execute(sql_select_query, {'id': discord_id})
    rows = db['cursor'].fetchall()
    if len(rows) > 0:
        return PoopUpgrade(rows[0])
    else:
        return PoopUpgrade((discord_id, 0))
