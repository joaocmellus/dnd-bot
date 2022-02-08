from discord.ext import commands
import os

# Importar cogs
from cogs.spells import Spells
from cogs.coin import Coin
from cogs.infos import Infos
from cogs.armors import Armors
from cogs.weapons import Weapons

bot = commands.Bot(command_prefix="!", case_insensitive=True)

# Adicionar Cogs
bot.add_cog(Spells(bot))
bot.add_cog(Coin(bot))
bot.add_cog(Infos(bot))
bot.add_cog(Armors(bot))
bot.add_cog(Weapons(bot))

# Adiciona evento
@bot.event
async def on_ready():
	print(f'Logged on as {bot.user}!')

# Iniciar o bot
if __name__ == '__main__':
	TOKEN = os.getenv('TOKEN')
	bot.run(TOKEN)