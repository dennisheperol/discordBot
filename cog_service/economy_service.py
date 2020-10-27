import time
from random import randrange
from typing import List

from domain.poop_balance import PoopBalance
from infrastructure.poop_balance_repo import poop_balance_repo
from infrastructure.poop_upgrade_repo import poop_upgrade_repo
from infrastructure.scavenge_time_repo import scavenge_time_repo


class EconomyService:
    @staticmethod
    def get_scavenge_time_seconds_passed(discord_id) -> int:
        scavenge_time = scavenge_time_repo.get_scavenge_time(discord_id)
        return int(time.time() - scavenge_time.time)

    def scavenge_poop(self, discord_id) -> (int, int):
        poop_amount, roll_modifier = self._calculate_scavenge_poop_amount(discord_id)
        self._increase_poop_balance(discord_id, poop_amount)
        self._set_scavenge_time_now(discord_id)
        return poop_amount, roll_modifier

    def give_poop_amount_to(self, giver_id, amount_to_give, taker_id):
        giver_poop_amount = self.get_poop_amount(giver_id)
        if giver_poop_amount < amount_to_give:
            return False, giver_poop_amount

        self._increase_poop_balance(taker_id, amount_to_give)
        giver_amount_left = self.decrease_poop_balance(giver_id, amount_to_give)
        return True, giver_amount_left

    @staticmethod
    def get_poop_amount(discord_id):
        return poop_balance_repo.get_poop_balance(discord_id).balance

    @staticmethod
    def get_ten_highest_poop_balances() -> List[PoopBalance]:
        return poop_balance_repo.get_highest_balances(10)

    @staticmethod
    def decrease_poop_balance(discord_id, poop_amount) -> int:
        poop_balance = poop_balance_repo.get_poop_balance(discord_id)
        poop_balance.decrease_balance(poop_amount)
        poop_balance_repo.set_poop_balance(poop_balance)
        return poop_balance.balance

    @staticmethod
    def _calculate_scavenge_poop_amount(discord_id) -> (int, int):
        poop_upgrade = poop_upgrade_repo.get_poop_upgrade(discord_id)
        roll_modifier = poop_upgrade.chance + 1
        poop_amount = randrange(roll_modifier) + 1
        return poop_amount, roll_modifier

    @staticmethod
    def _increase_poop_balance(discord_id, poop_amount) -> int:
        poop_balance = poop_balance_repo.get_poop_balance(discord_id)
        poop_balance.increase_balance(poop_amount)
        poop_balance_repo.set_poop_balance(poop_balance)
        return poop_balance.balance

    @staticmethod
    def _set_scavenge_time_now(discord_id) -> None:
        scavenge_time = scavenge_time_repo.get_scavenge_time(discord_id)
        scavenge_time.time = time.time()
        scavenge_time_repo.set_scavenge_time(scavenge_time)


economy_service = EconomyService()
