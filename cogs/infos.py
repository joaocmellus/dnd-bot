from .search import Search, read
from discord import Embed
from discord.ext import commands

class Infos(commands.Cog):
    def __init__(self):
        self._conditions = Search('conditions.json')
        self._wproperties = Search('weapons-properties.json')

    @commands.command(name = 'condição')
    async def condition(self, ctx, *, condition_name= None):
        if not condition_name:
            await ctx.send('Comando incompleto.')
            return
        condition = await self._conditions.get_data(condition_name)
        if not condition:
            await ctx.send('A condição  não foi encontrada.')
            return

        embed = Embed(title=condition['nome'], description= '• ' + '\n• '.join(condition['efeitos']))
        await ctx.send(embed=embed)

    @commands.command(name='condições')
    async def conditions(self, ctx):
        conditions = await self._conditions.get_all('nome')
        embed = Embed(title='Condições', description='• ' + '\n• '.join([i[0] for i in conditions]))
        await ctx.send(embed=embed)

    @commands.command(aliases = ['propriedade', 'info', 'i'])
    async def propertie(self, ctx, *, propertie_name= None):
        if not propertie_name:
            await ctx.send('Comando incompleto.')
            return
        propertie = await self._wproperties.get_data(propertie_name)
        if not propertie:
            await ctx.send('A propriedade não foi encontrada.')
            return
        embed = Embed(title=propertie['nome'], description= propertie['descrição'])
        await ctx.send(embed=embed)

    @commands.command(name='propriedades')
    async def properties(self, ctx):
        properties = await self._wproperties.get_all('nome')
        embed = Embed(title='Propriedades das Armas', description='• ' + '\n• '.join([i[0] for i in properties]))
        await ctx.send(embed=embed)