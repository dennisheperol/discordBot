import time
from random import randrange

import discord
from discord.ext import commands

import infrastructure.poop_balance_repo as poop_repo
import infrastructure.poop_upgrade_repo as upgrade_repo
import infrastructure.scavenge_time_repo as scavenge_repo


class Economy(commands.Cog):
    WAIT_TIME = 1800

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Economy loaded.')

    @commands.command()
    async def balance(self, ctx: commands.Context):
        poop_balance = poop_repo.get_poop_balance(ctx.author.id)
        await ctx.send(f'{ctx.author.mention} you have {poop_balance.balance} :poop:.')

    @commands.command()
    async def scavenge(self, ctx: commands.Context):
        scavenge_time = scavenge_repo.get_scavenge_time(ctx.author.id)
        seconds_passed = int(time.time() - scavenge_time.time)

        if seconds_passed < self.WAIT_TIME:
            minutes = int((self.WAIT_TIME - seconds_passed) / 60)
            seconds = (self.WAIT_TIME - seconds_passed) % 60
            await ctx.send(
                f'{ctx.author.mention} you have to wait {minutes} minute(s) {seconds} second(s) before you can scavenge again.')
            return

        poop_upgrade = upgrade_repo.get_poop_upgrade(ctx.author.id)
        amount = randrange(poop_upgrade.chance + 1) + 1

        poop_balance = poop_repo.get_poop_balance(ctx.author.id)
        poop_balance.increase_balance(amount)
        poop_repo.set_poop_balance(poop_balance)

        scavenge_time.set_time(time.time())
        scavenge_repo.set_scavenge_time(scavenge_time)
        await ctx.send(f'(d{poop_upgrade.chance + 1}) {ctx.author.mention} you found {amount} :poop:.')

    @commands.command()
    async def give(self, ctx: commands.Context, target_member: discord.Member, amount: int):
        if amount == 0:
            await ctx.send(
                f'{target_member.mention}, {ctx.author.mention} wants to let you know he doesn\'t give a shit.')
            return
        elif amount < 0:
            await ctx.send('Sure, we deal in :poop:. But it\'s pretty shitty to try to steal it from someone else')
            return
        if ctx.author.id == target_member.id:
            await ctx.send('Giving yourself some :poop:? Stinky.')
            return

        author_poop_balance = poop_repo.get_poop_balance(ctx.author.id)
        if author_poop_balance.balance < amount:
            await ctx.send(f'You only have {author_poop_balance.balance} :poop:, shithead.')
            return
        target_member_poop_balance = poop_repo.get_poop_balance(target_member.id)

        author_poop_balance.decrease_balance(amount)
        target_member_poop_balance.increase_balance(amount)
        poop_repo.set_poop_balance(author_poop_balance)
        poop_repo.set_poop_balance(target_member_poop_balance)

        await ctx.send(f'{ctx.author.mention} you gave {target_member.mention} {amount} :poop:.')

    @give.error
    async def give_error(self, ctx, error):
        await ctx.send('I did not understand that.\n**Usage**: give [@member] [amount]')

    @commands.command()
    async def leaderboard(self, ctx: commands.Context):
        top_ten_balances = poop_repo.get_top_balances()
        send_back = ''
        for idx, poop_balance in enumerate(top_ten_balances):
            send_back += f'**{idx + 1}.** <@!{poop_balance.id}>:\t{poop_balance.balance} :poop:\n'

        await ctx.send(send_back)


def setup(client):
    client.add_cog(Economy(client))
