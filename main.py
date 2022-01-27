from discord.ext import commands
from decouple import config

# Importar cogs
from cogs.Spells import Spells
from cogs.Coin import Coin
from cogs.Infos import Infos
from cogs.Armors import Armors
from cogs.Weapons import Weapons

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
	TOKEN = config('TOKEN')
	bot.run(TOKEN)