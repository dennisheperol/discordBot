import os

from discord.ext import commands

from secrets.secrets import discord_token

client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    print('Bot is ready.')


@client.command()
async def joke(ctx: commands.Context):
    await ctx.send('https://euw.op.gg/summoner/userName=PinguTilt')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(discord_token)
