import discord
from discord.ext import commands
import os

# Importing Cogs
from cogs.spells import Spells
from cogs.coin import Coin
from cogs.infos import Infos
from cogs.armors import Armors
from cogs.weapons import Weapons
from cogs.dice import Dice

# Intents
intents = discord.Intents.default()
intents.message_content = True

# Instantiating bot
bot = commands.Bot(command_prefix='!', case_insensitive=True, intents=intents)

# Events
@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')

# Add Cogs
@bot.event
async def on_connect():
    await bot.add_cog(Spells())
    await bot.add_cog(Coin())
    await bot.add_cog(Infos())
    await bot.add_cog(Armors())
    await bot.add_cog(Weapons())
    await bot.add_cog(Dice())

# Initiate bot
if __name__ == '__main__':
    TOKEN = os.getenv('TOKEN')
    bot.run(TOKEN)