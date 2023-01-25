import discord
from discord.ext import commands
import os

# Importing Cogs
from cogs.spells import Spells
from cogs.coin import Coin
from cogs.infos import Infos
from cogs.armors import Armors
from cogs.weapons import Weapons

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
    await bot.add_cog(Spells(bot))
    await bot.add_cog(Coin(bot))
    await bot.add_cog(Infos(bot))
    await bot.add_cog(Armors(bot))
    await bot.add_cog(Weapons(bot))   

# Iniciar o bot
if __name__ == '__main__':
    TOKEN = os.getenv('TOKEN')
    bot.run(TOKEN)