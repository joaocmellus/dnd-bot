from discord.ext import commands

class Coin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.coins = ('pc', 'pp', 'pe', 'po', 'pl')
        self.convertion = (
        # Ordem da seleção: coluna-linha
        #   pc      pp      pe      po    pl
            (1,     0.1,    0.02,   0.01,   0.001), # pc
            (10,    1,      0.2,    0.1,    0.01),  # pp 
            (50,    5,      1,      0.5,    0.05),  # pe
            (100,   10,     2,      1,      0.1),   # po
            (1000,  100,    20,     10,     1)      # pl
        )

    @commands.command(name = 'converter')
    async def convert_coin(self, ctx, value=None, to_coin=None):
        if not value or not to_coin:
            await ctx.send('Comando incompleto.')
            return
        to_coin = to_coin.lower()
        if to_coin not in self.coins:
            await ctx.send('Moeda inválida')
            return
        value = await self.format_coin(value)
        if not value:
            await ctx.send('Valor inválido!')
            return

        result = await self.convert(value, to_coin)
        if len(result) == 1:
            await ctx.send(f'> {value[0]}{value[1]} = {result[0]}{to_coin}')
        else:
            await ctx.send(f'> {value[0]}{value[1]} = {result[0]}{to_coin} e {result[1]}{value[1]}')

    async def format_coin(self, coin:str) -> tuple:
        """
        Recebe uma string 'ValorMoeda', verifica se é um valor 
        válido e retorna uma tupla com os valores separados.

        :param coin: str 'ValorMoeda'. Ex: '5po', '10pp'
        :return: tuple (valor, moeda). Ex: (5, 'po'), (10, 'pp')
        """
        value = coin[:-2]
        coin = coin[-2:].lower()
        if (coin in self.coins) and value.isdigit():
            return (int(value), coin)

    async def convert(self, coin:tuple, value:str) -> tuple:
        """
        Recebe uma tupla (valor, moeda) e um valor que ela será 
        convertida e retorna a uma tupla com os valores finais.
        
        :param coin: (valor, moeda)
        :param value: moeda que será convertida
        """
        index_coin = self.coins.index(coin[1])
        index_value = self.coins.index(value)
        convertion = self.convertion[index_coin][index_value]
        if convertion < 1:
            result = (int(coin[0] / convertion),)
        else:
            result = (coin[0] // convertion, coin[0] % convertion)

        return result

    @commands.command(name = 'pagar')
    async def pay(self, ctx, price = None, value = None):
        if not price or not value:
            await ctx.send('Há valores faltando!')
            return
        price = await self.format_coin(price)
        value = await self.format_coin(value)
        if not price or not value:
            await ctx.send('Valor inválido!')
            return
        converted = await self.convert(value, price[1])
        leftover = converted[0] - price[0]
        if leftover < 0:
            message = f'Dinheiro insuficiente. Faltam {leftover}{price[1]}'
        elif leftover == 0:
            if len(converted) == 2:
                message = f'Seu troco é de: {converted[1]}{value[1]}'
            else:
                message = f'Dinheiro correto! Não sobrou troco'
        else:
            reConvert = await self.convert((leftover, price[1]), value[1])
            if len(reConvert) == 1:
                if len(converted) == 1:
                    message = f'Seu troco é de: {reConvert[0]}{value[1]}'
                else:
                    message = f'Seu troco é de: {reConvert[0] + converted[1]}{value[1]}'
            else:
                if len(converted) == 1:
                    message = 'Seu troco é de: '
                    # verifica se foi possível converter o valor para um número inteiro, para não mostrar um resultado 0.
                    message += f'{reConvert[0]}{value[1]} e {reConvert[1]}{price[1]}' if (reConvert[0] != 0) else f'{reConvert[1]}{price[1]}'
                else:
                    message = f'Seu troco é de: {reConvert[0] + converted[1]}{value[1]} e {reConvert[1]}{price[1]}'

        await ctx.send(f'<@!{ctx.author.id}> ' + message)
