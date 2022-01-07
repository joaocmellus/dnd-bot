from discord.ext import commands

class CoinCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.coins = ('pc', 'pp', 'pe', 'po', 'pl')
		self.convertion = (
		# Ordem da seleção: coluna-linha
		#	pc		 pp		 pe		 po		 pl
			(1,		0.1,	0.02,	0.01,	0.001),	# pc
			(10,	1,		0.2,	0.1,	0.01 ),	# pp 
			(50,	5,		1,		0.5,	0.05 ),	# pe
			(100,	10,		2,		1,		0.1	 ),	# po
			(1000,	100,	20,		10,		1	 )	# pl
		)

	async def coin_splitter(self, coin) -> tuple:
		"""Recebe uma string 'valor'+'moeda', verifica e retorna uma tupla com os valores separados ou None"""
		value = coin[:-2]
		coin = coin[-2:].lower()
		if (coin in self.coins) and value.isdigit():
			return (int(value), coin)

	async def convert(self, coin:tuple, value:str) -> tuple:
		"""Recebe a tupla da moeda a ser convertida e a moeda final e retorna a uma tupla com os valores finais"""
		inserted_coin = self.coins.index(coin[1])
		final_coin = self.coins.index(value)
		convertion = self.convertion[final_coin][inserted_coin]

		if convertion < 1:
			result = (int(coin[0] / convertion),)

		else:
			result = (coin[0] // convertion, coin[0] % convertion)

		return result

	@commands.command(name = 'converter')
	async def converter(self, ctx, coin, to_coin):
		to_coin = to_coin.lower()
		if to_coin not in self.coins:
			await ctx.send('Moeda inválida')
			return

		coin = await self.coin_splitter(coin)
		if not coin:
			await ctx.send('Valor inválido!')
			return

		result = await self.convert(coin, to_coin)
		if len(result) == 1:
			await ctx.send(f'> {coin[0]}{coin[1]} = {result[0]}{to_coin}')
		else:
			await ctx.send(f'> {coin[0]}{coin[1]} = {result[0]}{to_coin} e {result[1]}{coin[1]}')

	@commands.command(name = 'pagar')
	async def pay(self, ctx, price = None, value = None):
		if not price or not value:
			await ctx.send('Há valores faltando!')
			return

		price = await self.coin_splitter(price)
		value = await self.coin_splitter(value)
		if not price or not value:
			await ctx.send('Valor inválido!')
			return

		converted = await self.convert(value, price[1])
		leftower = converted[0] - price[0]

		if leftower < 0:
			message = f'dinheiro insuficiente. Faltam {leftower}{price[1]}'

		elif leftower == 0:
			if len(converted) == 2:
				message = f'seu troco é de: {converted[1]}{value[1]}'
			else:
				message = f'dinheiro correto! Não sobrou troco'
			
		else:
			reConvert = await self.convert((leftower, price[1]), value[1])
			if len(reConvert) == 1:
				if len(converted) == 1:
					message = f'seu troco é de: {reConvert[0]}{value[1]}'
				else:
					message = f'seu troco é de: {reConvert[0] + converted[1]}{value[1]}'
			else:
				if len(converted) == 1:
					message = 'Seu troco é de: '
					# verifica se foi possível converter o valor para um número inteiro, para não mostrar um resultado 0.
					message += f'{reConvert[0]}{value[1]} e {reConvert[1]}{price[1]}' if (reConvert[0] != 0) else f'{reConvert[1]}{price[1]}'
				else:
					message = f'Seu troco é de: {reConvert[0] + converted[1]}{value[1]} e {reConvert[1]}{price[1]}'

		await ctx.send(f'<@!{ctx.author.id}> ' + message)