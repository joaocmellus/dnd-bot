from . import Search, read
from discord import Embed
from discord.ext import commands

class InfoData(Search):
	def __init__(self, data, data1):
		super().__init__(data)
		self.data1 = {i['nome'].lower() : i for i in read(data1)}

	async def get_data(self, name):
		name = name.lower()
		if name in self.data:
			return self.data.get(name)
		return self.data1.get(name, None)

class Infos(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.informations = InfoData('conditions.json', 'weapons-properties.json')

	@commands.command(aliases = ['i'])
	async def info(self, ctx, *, info = None):
		if not info:
			# Mensagem de erro
			await ctx.send('Comando incorreto...')
			return
		info = await self.informations.get_data(info)

		if not info:
			# Mensagem de erro
			await ctx.send('A condição não existe...')
			return

		if 'efeitos' in info:
			embed = Embed(title=info['nome'], description= '• ' + '\n• '.join(info['efeitos']))
		else:
			embed = Embed(title=info['nome'], description= info['descrição'])

		await ctx.send(embed=embed)