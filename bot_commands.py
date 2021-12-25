import discord
from main import bot
from infoRequests import SpellRequests

# EVENTOS
@bot.event
async def on_ready():
	print(f'Logged on as {bot.user}!')

@bot.event
async def on_message(message):
	if message.author == bot.user:	#Ignora as mensagens do próprio bot
		return
	await bot.process_commands(message)

# COMANDOS
# Pesquisar Magias
@bot.command(name = 'magia')
async def spell(ctx, *args):
	spell_name = ' '.join(args)
	data = await SpellRequests.get_spell(spell_name)
	# Criar embed com os dados do banco
	if not data:
		# MENSAGEM DE ERRO
		return
	# Formatar textos
	ritual = ' **(Ritual)**' if data[3] == 1 else ''
	description = data[9].replace('Em Níveis Superiores.', '**Em Níveis Superiores.**')
	if '\t' in description:
		description = list(description)
		x = False
		for i, j in enumerate(description):
			if j == '\t':
				description[i] = '\t**'
				x = True
			elif j == '.' and x == True:
				description[i] = '.**'
				x = False
		description = ''.join(description)

	# Verificar se a magia possui tabela
	if data[10] == 1:
		# Adicionar imagem
		print('tem imagem :)')
	embed = {
		'title': data[1],
		'description': str(data[2]) + 'º nível de ' + data[4] + ritual if data[2] != 0 else 'Truque de ' + data[4] + ritual, 
		'type': 'rich',  
		'fields': [
			{'inline': False, 'name': 'Conjuradores', 'value': ', '.join(data[12])}, 
			{'inline': False, 'name': 'Tempo de Conjuração', 'value': data[5]}, 
			{'inline': False, 'name': 'Alcance', 'value': data[6]}, 
			{'inline': False, 'name': 'Componentes', 'value': data[7]}, 
			{'inline': False, 'name': 'Duração', 'value': data[8]}, 
			{'inline': False, 'name': 'Descrição', 'value': description}
		], 
		'footer': {'text': 'Fonte: ' + data[11]},
	}
	embed = discord.Embed.from_dict(embed)
	embed.colour = colours[data[4]]
	await ctx.send(embed=embed)
# Cores para as magias
colours = {
	'abjuração': discord.Colour.blurple(),
	'adivinhação' : discord.Colour.gold(),
	'conjuração' : discord.Colour.blue(),
	'encantamento' : discord.Colour.purple(),
	'evocação' : discord.Colour.red(),
	'ilusão' : discord.Colour.light_gray(),
	'necromancia' : discord.Colour.darker_gray(),
	'transmutação' : discord.Colour.green()
}