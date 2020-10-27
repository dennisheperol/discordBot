from discord.ext import commands

from cog_service.shop_service import shop_service


class Shop(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Shop loaded.')

    @commands.command()
    async def upgrade(self, ctx: commands.Context, to_upgrade='', modifier=''):
        if to_upgrade == 'chance':
            await self._upgrade_chance(ctx, modifier)
            return

        upgrade_prices = shop_service.get_upgrade_prices(ctx.author.id)
        text_to_send = ''
        for upgrade in upgrade_prices:
            text_to_send += f'`upgrade {upgrade} [max]` ({upgrade_prices[upgrade]} :poop: for next upgrade)'
        await ctx.send(text_to_send)

    @staticmethod
    async def _upgrade_chance(ctx, modifier):
        status = shop_service.try_upgrade_chance(
            ctx.author.id, modifier)

        if not status.successful:
            await ctx.send(f'{ctx.author.mention}, you don''t have the necessary :poop: to upgrade.\n'
                           f'(next upgrade: {status.next_price} :poop:, current balance: {status.current_amount} :poop:)')
            return

        increment_text = f' {status.total_increment} times' if status.total_increment > 1 else ''
        await ctx.send(
            f'{ctx.author.mention}, you paid {status.spent_amount} :poop: to increase your chances{increment_text}.\n'
            f'(next upgrade: {status.next_price} :poop:, current balance: {status.current_amount} :poop:)')


def setup(client):
    client.add_cog(Shop(client))
