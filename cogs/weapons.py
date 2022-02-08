from .search import Search
from discord import Embed, Colour
from discord.ext import commands

class Weapons(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self._weapons = Search('weapons.json')

	@commands.command(name = 'arma')
	async def weapon(self, ctx, *, weapon_name = None):
		if not weapon_name:
			# Mensagem de erro
			await ctx.send('Comando incorreto...')
			return
		weapon = await self._weapons.get_data(weapon_name)

		if not weapon:
			# Mensagem de erro
			await ctx.send('A arma não existe...')
			return
		embed = Embed.from_dict({
			'title': weapon['nome'],
			'description': 'Arma ' + ' '.join(weapon['tipo']), 
			'type': 'rich',
			'fields': [
				{'inline': True, 'name': 'Dano', 'value': ' '.join(weapon['dano']) if all(weapon['dano']) else '–'}, 
				{'inline': True, 'name': 'Preço', 'value':weapon['preço']}, 
				{'inline': True, 'name': 'Peso', 'value': weapon['peso'] if weapon['peso'] != None else '–'}, 
				{'inline': False, 'name': 'Propriedades', 'value': '• ' + '\n• '.join([i.capitalize() for i in weapon['propriedades']])},
			]
		})
		embed.colour = Colour.dark_grey()
		await ctx.send(embed=embed)

	@commands.command(name = 'armas')
	async def weapons(self, ctx, wtype=None):
		weapons = await self._weapons.get_all('nome', 'tipo')
		if wtype == 'simples':
			embed = Embed.from_dict({
				'title': 'Armas Simples',
				'type': 'rich',
				'fields': [
					{'inline': True, 'name': 'Corpo-a-Corpo', 'value': '\n'.join([i[0] for i in weapons if i[1][0] == 'simples' and i[1][1] == 'corpo-a-corpo'])}, 
					{'inline': True, 'name': 'à Distância', 'value': '\n'.join([i[0] for i in weapons if i[1][0] == 'simples' and i[1][1] == 'distância'])}, 
				]
			})
		elif wtype == 'marcial' or wtype == 'marciais':
			embed = Embed.from_dict({
				'title': 'Armas Simples',
				'type': 'rich',
				'fields': [
					{'inline': True, 'name': 'Corpo-a-Corpo', 'value': '\n'.join([i[0] for i in weapons if i[1][0] == 'marcial' and i[1][1] == 'corpo-a-corpo'])}, 
					{'inline': True, 'name': 'à Distância', 'value': '\n'.join([i[0] for i in weapons if i[1][0] == 'marcial' and i[1][1] == 'distância'])}, 
				]
			})
		else:
			await ctx.send('Comando incorreto...')
			return

		embed.colour = Colour.dark_grey()		
		await ctx.send(embed=embed)