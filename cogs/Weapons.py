from . import Search
from discord import Embed, Colour
from discord.ext import commands

class Weapons(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.weapons = Search('weapons.json')

	@commands.command(name = 'arma')
	async def weapon(self, ctx, *, weapon_name = None):
		if not weapon_name:
			# Mensagem de erro
			await ctx.send('Comando incorreto...')
			return
		weapon = await self.weapons.get_data(weapon_name)

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