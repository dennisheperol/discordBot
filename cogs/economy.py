import discord
from discord.ext import commands

from cog_service.economy_service import economy_service


class Economy(commands.Cog):
    WAIT_TIME = 1800

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Economy loaded.')

    @commands.command()
    async def balance(self, ctx: commands.Context):
        poop_amount = economy_service.get_poop_amount(ctx.author.id)
        await ctx.send(f'{ctx.author.mention} you have {poop_amount} :poop:.')

    @commands.command()
    async def scavenge(self, ctx: commands.Context):
        seconds_passed = economy_service.get_scavenge_time_seconds_passed(ctx.author.id)
        if seconds_passed < self.WAIT_TIME:
            await self._send_wait_message(ctx, seconds_passed)
            return

        poop_amount, roll_modifier = economy_service.scavenge_poop(ctx.author.id)
        await ctx.send(f'(d{roll_modifier}) {ctx.author.mention} you found {poop_amount} :poop:.')

    @commands.command()
    async def give(self, ctx: commands.Context, target_member: discord.Member, amount: int):
        if amount == 0:
            await ctx.send(
                f'{target_member.mention}, {ctx.author.mention} wants to let you know he doesn\'t give a shit.')
            return
        elif amount < 0:
            await ctx.send(
                f'Sure {ctx.author.mention}, we deal in :poop:. But it\'s pretty shitty to try to steal it from someone else')
            return
        if ctx.author.id == target_member.id:
            await ctx.send(f'Giving yourself some :poop: {ctx.author.mention}? Stinky.')
            return

        success, author_amount_left = economy_service.give_poop_amount_to(ctx.author.id, amount, target_member.id)
        if success:
            await ctx.send(f'{ctx.author.mention} you gave {target_member.mention} {amount} :poop:.\n'
                           f'You have {author_amount_left} :poop: left.')
        else:
            await ctx.send(f'You only have {author_amount_left} :poop:, shithead.')

    @give.error
    async def give_error(self, ctx, error):
        await ctx.send('I did not understand that.\n**Usage**: give [@member] [amount]')

    @commands.command()
    async def leaderboard(self, ctx: commands.Context):
        highest_balances = economy_service.get_ten_highest_poop_balances()
        leaderboard_message = await self._format_leaderboard_message(ctx, highest_balances)
        await ctx.send(leaderboard_message)

    @staticmethod
    async def _format_leaderboard_message(ctx, highest_balances):
        converter = commands.MemberConverter()
        send_back = ''
        for idx, poop_balance in enumerate(highest_balances):
            member = await converter.convert(ctx, f'<@!{poop_balance.id}>')
            send_back += f'{idx + 1}. {member.name}\t{poop_balance.balance} :poop:\n'
        return send_back

    async def _send_wait_message(self, ctx, seconds_passed):
        minutes, seconds = divmod(self.WAIT_TIME - seconds_passed, 60)
        await ctx.send(f'{ctx.author.mention} you have to wait {minutes} minute(s) {seconds} second(s) '
                       f'before you can scavenge again.')


def setup(client):
    client.add_cog(Economy(client))
