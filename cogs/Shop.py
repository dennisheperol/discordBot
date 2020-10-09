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
    async def upgrade(self, ctx: commands.Context, to_upgrade=''):
        chance = upgrade_repo.get_poop_upgrade(ctx.author.id)['chance']

        if to_upgrade == 'chance':
            await self._upgrade_chance(ctx, chance)
            return

        chance_price = self._calculate_chance_price(chance)
        await ctx.send(f'.upgrade chance  ({chance_price} :poop:)')

    async def _upgrade_chance(self, ctx, chance):
        poop_balance = poop_repo.get_poop_balance(ctx.author.id)
        chance_price = self._calculate_chance_price(chance)

        if poop_balance < chance_price:
            await ctx.send(f'{ctx.author.mention}, you don''t have the necessary funds to upgrade.')
            return

        poop_repo.increase_poop_balance(ctx.author.id, -chance_price)
        upgrade_repo.increase_poop_chance(ctx.author.id)
        await ctx.send(f'{ctx.author.mention}, you paid {chance_price} :poop: to increase your chances.')

    @staticmethod
    def _calculate_chance_price(chance):
        chance = chance + 1
        return math.ceil(chance * (math.log10(chance) ** 2))


def setup(client):
    client.add_cog(Shop(client))
