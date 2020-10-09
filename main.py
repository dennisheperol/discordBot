import os

from discord.ext import commands
import discord

from secrets.secrets import discord_token

intents = discord.Intents.default()
intents.members = True  # Subscribe to the privileged members intent.
client = commands.Bot(command_prefix='.', intents=intents)


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
