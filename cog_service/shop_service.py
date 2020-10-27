import math
from typing import Dict

from cog_service.economy_service import economy_service
from infrastructure.poop_upgrade_repo import poop_upgrade_repo


class UpgradeStatus:
    def __init__(self, successful, total_increment, spent_amount, current_amount, next_price):
        self.successful = successful
        self.total_increment = total_increment
        self.spent_amount = spent_amount
        self.current_amount = current_amount
        self.next_price = next_price


class ShopService:
    def get_upgrade_prices(self, discord_id) -> Dict[str, int]:
        poop_upgrade = poop_upgrade_repo.get_poop_upgrade(discord_id)
        return {'chance': self._calculate_next_chance_price(poop_upgrade.chance)}

    def try_upgrade_chance(self, discord_id, modifier) -> UpgradeStatus:
        poop_amount = economy_service.get_poop_amount(discord_id)
        poop_upgrade = poop_upgrade_repo.get_poop_upgrade(discord_id)
        chance_price = self._calculate_next_chance_price(poop_upgrade.chance)

        if poop_amount < chance_price:
            return UpgradeStatus(False, 0, 0, poop_amount, chance_price)

        increment = 1
        if modifier == 'max':
            chance_price, increment = self._calculate_max_chance(poop_amount, poop_upgrade.chance)

        poop_amount = economy_service.decrease_poop_balance(discord_id, chance_price)
        poop_upgrade = self._upgrade_chance(discord_id, increment)
        next_chance_price = self._calculate_next_chance_price(poop_upgrade.chance)
        return UpgradeStatus(True, increment, chance_price, poop_amount, next_chance_price)

    @staticmethod
    def _upgrade_chance(discord_id, increment=1):
        poop_upgrade = poop_upgrade_repo.get_poop_upgrade(discord_id)
        poop_upgrade.increase_chance(increment)
        poop_upgrade_repo.set_poop_upgrade(poop_upgrade)
        return poop_upgrade

    def _calculate_max_chance(self, current_balance, current_chance):
        total_price = 0
        total_increment = 0
        while total_price + self._calculate_next_chance_price(current_chance + total_increment) <= current_balance:
            total_price += self._calculate_next_chance_price(current_chance + total_increment)
            total_increment += 1
        return total_price, total_increment

    @staticmethod
    def _calculate_next_chance_price(chance) -> int:
        chance = chance + 1
        return math.ceil(chance * (math.log10(chance) ** 2))


shop_service = ShopService()
