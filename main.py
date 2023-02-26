import os
import discord
from discord.ext import commands
from data_handler import DataRepository, read_tables

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
db = DataRepository()
db.add_dir(os.path.join(os.path.dirname(__file__), 'data'), 'nome')

# Events
@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')

# Add Cogs
@bot.event
async def on_connect():
    await bot.add_cog(Spells(db, read_tables()))
    await bot.add_cog(Coin())
    await bot.add_cog(Infos(db))
    await bot.add_cog(Armors(db))
    await bot.add_cog(Weapons(db))
    await bot.add_cog(Dice())

# Initiate bot
if __name__ == '__main__':
    TOKEN = os.getenv('TOKEN')
    bot.run(TOKEN)