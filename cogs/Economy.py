from discord.ext import commands
from random import randrange
import time
import discord
import infrastructure.poop_balance_repo as poop_repo
import infrastructure.scavenge_time_repo as scavenge_repo


class Economy(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Economy loaded.')

    @commands.command()
    async def balance(self, ctx: commands.Context):
        balance = poop_repo.get_poop_balance(ctx.author.id)
        await ctx.send(f'{ctx.author.mention} you have {balance} :poop:.')

    @commands.command()
    async def scavenge(self, ctx: commands.Context):
        last_time = scavenge_repo.get_scavenge_time(ctx.author.id)
        seconds_passed = int(time.time() - last_time)
        if seconds_passed < 600:
            await ctx.send(f'{ctx.author.mention} you have to wait {600 - seconds_passed} seconds before you can scavenge again.')
            return

        amount = randrange(10) + 1
        poop_repo.increase_poop_balance(ctx.author.id, amount)
        scavenge_repo.set_scavenge_time(ctx.author.id, time.time())
        await ctx.send(f'{ctx.author.mention} you found {amount} :poop:.')


    @commands.command()
    async def give(self, ctx: commands.Context, member: discord.Member, amount: int):
        if amount == 0:
            await ctx.send(f'{member.mention}, {ctx.author.mention} wants to let you know he doesn''t give a shit.')
            return
        elif amount < 0:
            await ctx.send('Sure, we deal in :poop:. But it''s pretty shitty to try to steal it from someone else')
            return
        if ctx.author.id == member.id:
            await ctx.send('Giving yourself some :poop:? Stinky.')
            return

        own_amount = poop_repo.get_poop_balance(ctx.author.id)
        if own_amount < amount:
            await ctx.send(f'You only have {own_amount} :poop:, shithead.')
            return

        poop_repo.increase_poop_balance(member.id, amount)
        poop_repo.increase_poop_balance(ctx.author.id, -amount)

        await ctx.send(f'{ctx.author.mention} you gave {member.mention} {amount} :poop:.')

    @give.error
    async def give_error(self, ctx, error):
        await ctx.send('I did not understand that.\n**Usage**: give [@member] [amount]')


def setup(client):
    client.add_cog(Economy(client))