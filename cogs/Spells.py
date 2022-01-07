from . import read
from discord import Colour, Embed
from discord.ext import commands

class Spells:
	def __init__(self):
		self.spells = tuple(read('spells.json'))
		self.spellNames = tuple([s['nome'].lower() for s in self.spells])
		self.classes = read('spells-class.json')

	async def get_spell(self, spell_name):
		spell_name = spell_name.lower()

		if spell_name in self.spellNames:
			s = self.spellNames.index(spell_name)
			return self.spells[s]

	async def get_class(self, class_name):
		class_name = class_name.lower()

		if class_name in self.classes:
			return self.classes[class_name]

class SpellsCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.spells = Spells()
		# Cores para cada tipo de magia
		self.colours = {
			'abjuração': Colour.blurple(),
			'adivinhação' : Colour.gold(),
			'conjuração' : Colour.blue(),
			'encantamento' : Colour.purple(),
			'evocação' : Colour.red(),
			'ilusão' : Colour.light_gray(),
			'necromancia' : Colour.darker_gray(),
			'transmutação' : Colour.green()
		}

	@commands.command(name = 'magia')
	async def spell(self, ctx, *, spell_name = None):
		if not spell_name:
			# Mensagem de erro
			await ctx.send('Comando incorreto...')
			return
		spell = await self.spells.get_spell(spell_name.lower())

		if not spell:
			# Mensagem de erro
			await ctx.send('A magia não existe...')
			return

		await self.send_spell(ctx, spell)

	async def send_spell(self, ctx, spell):
		"""Formata os dados da magia e envia no chat"""
		ritual = ' **(Ritual)**' if spell['ritual'] else ''
		description = await self.format_spell(spell['descrição'])

		# description_list = await self.format_spell(spell['descrição'])
		# Loop para criar embeds
		# for i, description in enumerate(descriptions):
		# 	if i == 0:

		# Cria o Embed
		embed = {
			'title': spell['nome'],
			'description': str(spell['nível']) + 'º nível de ' + spell['escola'] + ritual if spell['nível'] != 0 else 'Truque de ' + spell['escola'], 
			'type': 'rich',
			'fields': [
				{'inline': False, 'name': 'Conjuradores', 'value': ', '.join(spell['classes'])}, 
				{'inline': False, 'name': 'Tempo de Conjuração', 'value': spell['tempo de conjuração']}, 
				{'inline': False, 'name': 'Alcance', 'value': spell['alcance']}, 
				{'inline': False, 'name': 'Componentes', 'value': spell['componentes']}, 
				{'inline': False, 'name': 'Duração', 'value': spell['duração']}, 
				{'inline': False, 'name': 'Descrição', 'value': description},
			],
			'footer': {'text': 'Fonte: ' + spell['fonte']},
		}
		embed = Embed.from_dict(embed)
		embed.colour = self.colours[spell['escola']]

		await ctx.send(embed=embed)

		# Verificar se tem tabela...

	async def format_spell(self, text:str) -> list:
		text = text.replace('Em Níveis Superiores.', '**Em Níveis Superiores.**')
		if '\t' in text:
			text = list(text)
			x = False
			for i, j in enumerate(text):
				if j == '\t':
					text[i] = '\t**'
					x = True
				elif j == '.' and x == True:
					text[i] = '.**'
					x = False
			text = ''.join(text)

		# Verificar se o texto cabe no embed
		# if len(text) > 1024:
		# 	text = await self.text_splitter(text)
		# else:
			# text = [text]

		return text

	async def format_class(self, text) -> list:
		pass

	async def text_splitter(self, text) -> list:
		"""Reparte o texto para ser enviado em diferentes embeds, para suprir o limite máximo de caracteres"""
		# valor no field: 1024
		# valor da descrição: 4096
		pass