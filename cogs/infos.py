from .search import Search, read
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

	async def get_all(self, data, *args):
		if data == 'conditions':
			data = self.data.values()
		else:
			data = self.data1.values()
		return [tuple(v[k] for k in args) for v in data]

class Infos(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self._informations = InfoData('conditions.json', 'weapons-properties.json')

	@commands.command(aliases = ['i'])
	async def info(self, ctx, *, info = None):
		if not info:
			# Mensagem de erro
			await ctx.send('Comando incorreto...')
			return
		info = await self._informations.get_data(info)

		if not info:
			# Mensagem de erro
			await ctx.send('A condição não existe...')
			return

		if 'efeitos' in info:
			embed = Embed(title=info['nome'], description= '• ' + '\n• '.join(info['efeitos']))
		else:
			embed = Embed(title=info['nome'], description= info['descrição'])

		await ctx.send(embed=embed)

	@commands.command(name='condições')
	async def conditions(self, ctx):
		conditions = await self._informations.get_all('conditions', 'nome')

		embed = Embed(tittle='Condições', description='• ' + '\n• '.join([i[0] for i in conditions]))
		
		await ctx.send(embed=embed)

	@commands.command(name='propriedades')
	async def properties(self, ctx):
		properties = await self._informations.get_all('properties', 'nome')

		embed = Embed(tittle='Propriedades', description='• ' + '\n• '.join([i[0] for i in properties]))
		
		await ctx.send(embed=embed)

