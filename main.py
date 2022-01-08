import discord
from discord.ext import commands
from decouple import config

# Importar cogs
from cogs.Spells import SpellsCog
from cogs.Coin import CoinCog

bot = commands.Bot(command_prefix="!", case_insensitive=True)

# Adicionar Cogs
bot.add_cog(SpellsCog(bot))
bot.add_cog(CoinCog(bot))

# Adiciona evento
@bot.event
async def on_ready():
	print(f'Logged on as {bot.user}!')

# Iniciar o bot
if __name__ == '__main__':
	TOKEN = config('TOKEN')
	bot.run(TOKEN)