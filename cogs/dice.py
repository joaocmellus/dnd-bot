from discord.ext import commands
import random

class Dice(commands.Cog):
	@commands.command(name= 'rolar', aliases=['r', 'd', 'dado'])
	async def roll_dice(self, ctx, dice_expression=None):
		if not dice_expression:
			await ctx.send('Comando incompleto.')
			return
		if '+' in dice_expression:
			modifier = '+'
		else:
			modifier = '-'
		expressions = dice_expression.split(modifier)
		values = await split_dice(expressions[0].lower())
		if not values:
			ctx.send('Comando incorreto.')
			return
		if values[0] > 20:
			await ctx.send('Número máximo de rolagens por comando excedido. (máx de 20)')
			return
		if values[1] > 1000:
			await ctx.send('Valor máximo para o dado excedido. (máx de 1000)')
			return
		rolls = await roll(values[0],values[1])
		result = sum(rolls)
		if len(expressions) == 2:
			value = expressions[1].strip()
			if not value.isdigit():
				ctx.send('Modificador incorreto.')
			if modifier == '+':
				result += int(value)
			else:
				result -= int(value)
		await ctx.send(f'<@!{ctx.author.id}> seu resultado é: {result} nas rolagens ' + str(rolls))

async def split_dice(dice_value) -> bool or list:
	if not 'd' in dice_value:
		return
	values = dice_value.split('d')
	for i, value in enumerate(values):
		if i > 1:
			return
		value = value.strip()
		if not value:
			if i == 1:
				value = 6
			else:
				value = 1
		elif not value.isdigit():
			return
		values[i] = int(value)
	return values

async def roll(time, dice_value):
	rolls = []
	for i in range(time):
		value = random.randint(1, dice_value)
		rolls.append(value)

	return rolls