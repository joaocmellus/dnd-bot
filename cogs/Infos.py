from . import Search
from discord import Embed
from discord.ext import commands

class Infos(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.conditions = Search('conditions.json')

	@commands.command(aliases = ['i'])
	async def info(self, ctx, *, info = None):
		if not info:
			# Mensagem de erro
			await ctx.send('Comando incorreto...')
			return
		info = await self.conditions.get_data(info)

		if not info:
			# Mensagem de erro
			await ctx.send('A condição não existe...')
			return

		embed = Embed(title=info['nome'], description= '• ' + '\n• '.join(info['efeitos']))		
		await ctx.send(embed=embed)