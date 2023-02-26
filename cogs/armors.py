from discord import Embed, Colour
from discord.ext import commands

class Armors(commands.Cog):
    def __init__(self, data):
        self._armors = data.armors

    @commands.command(name = 'armadura')
    async def armor(self, ctx, *, armor_name = None):
        if not armor_name:
            await ctx.send('Comando incompleto.')
            return
        armor = await self._armors.get(armor_name)
        if not armor:
            await ctx.send('A armadura não foi encontrada.')
            return
        embed = Embed(
            title= armor['nome'], 
            colour= Colour.darker_grey(),
            description= 'Armadura ' + armor['tipo'] if 
                armor['tipo'] != 'escudo' else armor['tipo'],
        )
        fields = [
            ('CA', armor['CA']), 
            ('Preço', armor['preço']), 
            ('Peso', armor['peso']),
            ( 'Força mínima', '–' if not armor['força'] else armor['força']), 
            ('Furtividade', 'Desvantagem' if armor['desvantagem'] else '–'),
        ]
        for i in fields:
            embed.add_field(name=i[0], value=i[1])
        await ctx.send(embed=embed)

    @commands.command(name = 'armaduras')
    async def armors(self, ctx):
        armors = await self._armors.all('nome', 'tipo')
        embed = Embed(
            title= 'Armaduras', 
            colour= Colour.darker_grey(),
        )
        fields = [
            ('Leves', '\n'.join([i[0] for i in armors if i[1] == 'leve'])), 
            ('Médias', '\n'.join([i[0] for i in armors if i[1] == 'média'])),
            ('Pesadas', '\n'.join([i[0] for i in armors if i[1] == 'pesada'])),
            ('Escudos', '\n'.join([i[0] for i in armors if i[1] == 'escudo']))
        ]
        for i in fields:
            embed.add_field(name=i[0], value=i[1])
        embed.colour = Colour.dark_grey()
        
        await ctx.send(embed=embed)