from . import Search, read_tables
from discord import Colour, Embed, File
from discord.ext import commands

class Spells(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.spells = Search('spells.json')

		# Dicionário com as imagens que serão usadas nos embeds
		self.tables = {file[0][:-4].replace('_', ' ') : File(file[1], filename= file[0]) for file in read_tables()}

		# Cores para cada escola de magia
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
		spell = await self.spells.get_data(spell_name)

		if not spell:
			# Mensagem de erro
			await ctx.send('A magia não existe...')
			return

		await self.send_spell(ctx, spell)

	async def send_spell(self, ctx, spell):
		"""Formata os dados da magia e envia no chat"""
		ritual = ' **(Ritual)**' if spell['ritual'] else ''
		description_list = await self.format_spell(spell['descrição'])

		# Loop para criar embeds
		embeds = []

		# Cria o Embed
		for i, description in enumerate(description_list):
			if i == 0:
				embeds.append({
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
				})
			else:
				embeds.append({
					'title': spell['nome'] + ' - Continuação' ,
					'description': description, 
					'type': 'rich',
					'fields': [],
					'footer': {'text': 'Fonte: ' + spell['fonte']},
				})
		
		for i, embed in enumerate(embeds):
			embed = Embed.from_dict(embed)
			embed.colour = self.colours[spell['escola']]
			# Verifica e adiciona imagem da tabela ao embed
			if i == 0 and spell['tabela']:					# Primeira opção: enviar a imagem acoplada ao embed
				file = self.tables[spell['nome'].lower()]
				embed.set_image(url="attachment://" + file.filename)
				await ctx.send(embed=embed, file = file)
				continue
			await ctx.send(embed=embed)
			# if i == 0 and spell['tabela']:				# Segunda opção: enviar a imagem após o embed
			# 	file = self.tables[spell['nome'].lower()]
			# 	await ctx.send(file = file)

	async def format_spell(self, text:str) -> list:
		"""Formata a descrição da magia para o discord"""
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
		if len(text) > 1024:
			text = await self.text_splitter(text)
		else:
			text = [text]

		return text

	async def format_class(self, text) -> list:
		pass

	async def text_splitter(self, text) -> list:
		"""Reparte o texto para ser enviado em diferentes embeds, para suprir o limite máximo de caracteres"""
		splitted = text.split('\n')
		result = []

		for i, part in enumerate(splitted):
			#  Verificar se é o primeiro
			if i == 0:
				# Definir variável text
				text = part
				continue

			# Definir variável length
			if len(result) == 0:
				length = 1024	# valor do field
			else:
				length = 4096	# valor da descrição

			# Verificar o tamanho
			if len(text)+1 + len(part) > length:
				result.append(text)
				text = part
			else:
				text += '\n' + part
			
			# Verificar se é o último
			if i+1 == len(splitted):
				result.append(text)

		return result