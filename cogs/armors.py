from .search import Search
from discord import Embed, Colour
from discord.ext import commands

class Armors(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.armors = Search('armors.json')

	@commands.command(name = 'armadura')
	async def armor(self, ctx, *, armor_name = None):
		if not armor_name:
			# Mensagem de erro
			await ctx.send('Comando incorreto...')
			return
		armor = await self.armors.get_data(armor_name)

		if not armor:
			# Mensagem de erro
			await ctx.send('A armadura não existe...')
			return
		embed = Embed.from_dict({
			'title': armor['nome'],
			'description': 'Armadura ' + armor['tipo'] if armor['tipo'] != 'escudo' else armor['tipo'], 
			'type': 'rich',
			'fields': [
				{'inline': True, 'name': 'Classe de Armadura', 'value': armor['CA']}, 
				{'inline': True, 'name': 'Preço' , 'value': armor['preço']}, 
				{'inline': True, 'name': 'Peso', 'value': armor['peso']},
				{'inline': True, 'name': 'Força mínima', 'value': '–' if not armor['força'] else armor['força']}, 
				{'inline': True, 'name': 'Furtividade', 'value': 'Desvantagem' if armor['desvantagem'] else '–'},
			]
		})
		embed.colour = Colour.dark_grey()
		await ctx.send(embed=embed)

	@commands.command(name = 'armaduras')
	async def armors(self, ctx):
		armors = await self.armors.get_all('nome', 'tipo')

		embed = Embed.from_dict({
			'title': 'Armaduras',
			'type': 'rich',
			'fields': [
				{'inline': True, 'name': 'Leves', 'value': '\n'.join([i[0] for i in armors if i[1] == 'leve'])}, 
				{'inline': True, 'name': 'Médias', 'value': '\n'.join([i[0] for i in armors if i[1] == 'média'])}, 
				{'inline': True, 'name': 'Pesadas', 'value': '\n'.join([i[0] for i in armors if i[1] == 'pesada'])}, 
				{'inline': True, 'name': 'Escudos', 'value': '\n'.join([i[0] for i in armors if i[1] == 'escudo'])}, 
			]
		})
		embed.colour = Colour.dark_grey()
		
		await ctx.send(embed=embed)