import discord
from decouple import config
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

# Classe principal do Bot
bot = commands.Bot(command_prefix="!", case_insensitive=True, intents=intents)

from bot_commands import *

if __name__ == '__main__':
	TOKEN = config('TOKEN')
	bot.run(TOKEN)