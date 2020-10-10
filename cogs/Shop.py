import math

from discord.ext import commands

import infrastructure.poop_balance_repo as poop_repo
import infrastructure.poop_upgrade_repo as upgrade_repo


class Shop(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Shop loaded.')

    @commands.command()
    async def upgrade(self, ctx: commands.Context, to_upgrade='', modifier=''):
        poop_upgrade = upgrade_repo.get_poop_upgrade(ctx.author.id)

        if to_upgrade == 'chance':
            await self._upgrade_chance(ctx, poop_upgrade, modifier)
            return

        chance_price = self._calculate_next_chance_price(poop_upgrade.chance)
        await ctx.send(f'`.upgrade chance [max]` ({chance_price} :poop: for next upgrade)')

    async def _upgrade_chance(self, ctx, poop_upgrade, modifier):
        poop_balance = poop_repo.get_poop_balance(ctx.author.id)
        chance_price = self._calculate_next_chance_price(poop_upgrade.chance)

        if poop_balance.balance < chance_price:
            await ctx.send(f'{ctx.author.mention}, you don''t have the necessary :poop: to upgrade.')
            return

        increment = 1
        if modifier == 'max':
            chance_price, increment = self._calculate_max_chance(poop_balance.balance, poop_upgrade.chance)

        poop_balance.decrease_balance(chance_price)
        poop_repo.set_poop_balance(poop_balance)

        poop_upgrade.increase_chance(increment)
        next_price = self._calculate_next_chance_price(poop_upgrade.chance)
        upgrade_repo.set_poop_upgrade(poop_upgrade)

        increment_text = f' {increment} times' if increment > 1 else ''

        await ctx.send(
            f'{ctx.author.mention}, you paid {chance_price} :poop: to increase your chances{increment_text}.\n'
            f'(next upgrade: {next_price} :poop:, current balance: {poop_balance.balance} :poop:)')

    @staticmethod
    def _calculate_next_chance_price(chance):
        chance = chance + 1
        return math.ceil(chance * (math.log10(chance) ** 2))

    def _calculate_max_chance(self, current_balance, current_chance):
        total_price = 0
        total_increment = 0
        while total_price + self._calculate_next_chance_price(current_chance + total_increment) <= current_balance:
            total_price += self._calculate_next_chance_price(current_chance + total_increment)
            total_increment += 1
        return total_price, total_increment


def setup(client):
    client.add_cog(Shop(client))
