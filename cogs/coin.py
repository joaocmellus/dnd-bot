from discord.ext import commands

class Coin(commands.Cog):
    def __init__(self):
        self.converter = CoinConverter()

    @commands.command(name = 'converter')
    async def convert_coin(self, ctx, value=None, to_coin=None):
        if not value or not to_coin:
            await ctx.send('Comando incompleto.')
            return
        to_coin = to_coin.lower()
        if to_coin not in self.converter.coins:
            await ctx.send('Moeda inválida')
            return
        value = await self.converter.format_coin(value)
        if not value:
            await ctx.send('Valor inválido!')
            return
        results = await self.converter.convert(value, to_coin)
        for result in results:
            if result[0] == 0:
                del results[results.index(result)]
        if len(results) == 1:
            await ctx.send('> {}{} = {}{}'.format(*value, *results[0]))
        else:
            await ctx.send('> {}{} = {}{} e {}{}'.format(*value,*results[0],*results[1]))

class CoinConverter:
    def __init__(self):
        self.coins = ('pc', 'pp', 'pe', 'po', 'pl')
        self.convertion = ( # Ordem da conversão: coluna-linha
        #   pc      pp      pe      po      pl   
            (1,      10,    20,     100,    1000),  # pc
            (0.1,    1,     2,      10,     100 ),  # pp
            (0.05,   0.5,   1,      5,      50  ),  # pe
            (0.01,   0.1,   0.2,    1,      10  ),  # po
            (0.001,  0.01,  0.02,   0.1,    1   )   # pl
        )

    async def format_coin(self, coin:str) -> list:
        """
        Recebe uma string 'ValorMoeda', verifica se é um valor 
        válido e retorna uma tupla com os valores separados.

        :param coin: <str> 'ValorMoeda'. Ex: '5po', '10pp'
        :return: <tuple> (valor, moeda). Ex: (5, 'po'), (10, 'pp')
        """
        value = coin[:-2]
        coin = coin[-2:].lower()
        if (coin in self.coins) and value.isdigit():
            return [int(value), coin]

    async def convert(self, amount:list, coin:str) -> list:
        """
        Recebe uma tupla (valor, moeda) e um valor que ela será 
        convertida e retorna a uma tupla com os valores finais.
        
        :param coin: <tuple> (valor, moeda)
        :param value: <str> moeda que será convertida
        """
        amount_index = self.coins.index(amount[1])
        coin_index = self.coins.index(coin)
        convertion = self.convertion[amount_index][coin_index]

        result = []
        result.append([int(amount[0]/convertion), coin])
        
        if convertion > 1:
            if amount[0] % convertion:
                result.append([amount[0] % convertion, amount[1]])

        return result