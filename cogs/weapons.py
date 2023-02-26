from discord import Embed, Colour
from discord.ext import commands

class Weapons(commands.Cog):
    def __init__(self, data):
        self._weapons = data.weapons

    @commands.command(name = 'arma')
    async def weapon(self, ctx, *, weapon_name= None):
        if not weapon_name:
            await ctx.send('Comando incompleto.')
            return
        weapon = await self._weapons.get(weapon_name)
        if not weapon:
            await ctx.send('A arma não foi encontrada.')
            return

        # Enviar Embed
        embed = Embed(
            title= weapon['nome'], 
            colour= Colour.darker_gray(),
            description= 'Arma ' + ' '.join(weapon['tipo']), 
        )
        fields = [
            ('Dano', ' '.join(weapon['dano']) if all(weapon['dano']) else '–', True), 
            ('Preço', weapon['preço'], True), 
            ('Peso', weapon['peso'] if weapon['peso'] != None else '–', True), 
            ('Propriedades', '• ' + '\n• '.join([i.capitalize() for i in 
            weapon['propriedades']]), False)
        ]
        for i in fields:
            embed.add_field(name=i[0], value=i[1], inline=i[2])
        await ctx.send(embed=embed)
            
    @commands.command(name = 'armas')
    async def weapons(self, ctx, weapon_type=None):
        weapons = await self._weapons.all('nome', 'tipo')
        if weapon_type == 'simples':
            title = 'Armas Simples',
            fields = [
                ('Corpo-a-Corpo', '\n'.join([i[0] for i in weapons if i[1][0] == 'simples' and i[1][1] == 'corpo-a-corpo'])),
                ('à Distância', '\n'.join([i[0] for i in weapons if i[1][0] == 'simples' and i[1][1] == 'distância'])), 
            ]

        elif weapon_type == 'marcial' or weapon_type == 'marciais':
            title = 'Armas Simples',
            fields= [
                ('Corpo-a-Corpo', '\n'.join([i[0] for i in weapons if i[1][0] == 'marcial' and i[1][1] == 'corpo-a-corpo'])), 
                ('à Distância', '\n'.join([i[0] for i in weapons if i[1][0] == 'marcial' and i[1][1] == 'distância'])) 
            ]
        elif weapon_type == None:
            title = 'Armas Simples e Marciais'
            fields = [
                ('Simples Corpo-a-Corpo', '\n'.join([i[0] for i in weapons if i[1][0] == 'simples' and i[1][1] == 'corpo-a-corpo'])), 
                ('Simples à Distância', '\n'.join([i[0] for i in weapons if i[1][0] == 'simples' and i[1][1] == 'distância'])),
                ('', ''),
                ('Marcial Corpo-a-Corpo', '\n'.join([i[0] for i in weapons if i[1][0] == 'marcial' and i[1][1] == 'corpo-a-corpo'])), 
                ('Marcial à Distância', '\n'.join([i[0] for i in weapons if i[1][0] == 'marcial' and i[1][1] == 'distância'])),
                ('', '')
            ]
        else:
            await ctx.send('Comando incorreto.')
            return
        embed = Embed(title=title, colour=Colour.darker_gray())
        for i in fields:
            embed.add_field(name=i[0], value=i[1])
        await ctx.send(embed=embed)