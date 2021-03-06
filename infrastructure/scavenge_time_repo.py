from domain.scavenge_time import ScavengeTime
from infrastructure.helpers import wrapper


class ScavengeTimeRepo:
    def set_scavenge_time(self, scavenge_time: ScavengeTime):
        wrapper(self._set_scavenge_time_func, scavenge_time)

    def get_scavenge_time(self, discord_id) -> ScavengeTime:
        return wrapper(self._get_scavenge_time_func, discord_id)

    @staticmethod
    def _set_scavenge_time_func(db, scavenge_time: ScavengeTime):
        sql_update_query = """INSERT INTO scavenge_time (id, time) VALUES (%(id)s,%(time)s)
        ON CONFLICT (id) DO
        UPDATE SET time = %(time)s"""
        db['cursor'].execute(sql_update_query, {'id': scavenge_time.id, 'time': scavenge_time.time})
        db['connection'].commit()

    @staticmethod
    def _get_scavenge_time_func(db, discord_id) -> ScavengeTime:
        sql_select_query = """SELECT * FROM scavenge_time WHERE id = %(id)s"""
        db['cursor'].execute(sql_select_query, {'id': discord_id})
        rows = db['cursor'].fetchall()
        if len(rows) > 0:
            return ScavengeTime(rows[0])
        else:
            return ScavengeTime((discord_id, 0))


scavenge_time_repo = ScavengeTimeRepo()
