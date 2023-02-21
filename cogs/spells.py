from .search import Search, read_tables
from discord import Colour, Embed, File
from discord.ext import commands

class Spells(commands.Cog):
    def __init__(self):
        self._spells = Search('spells.json')
        self.tables = [File(file, filename= f'tabela {iteration+1}.png') for iteration, file in enumerate(read_tables())]
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
    async def spell(self, ctx, *, spell_name= None):
        if not spell_name:
            await ctx.send('Comando incompleto.')
            return
        spell = await self._spells.get_data(spell_name.lower())
        if not spell:
            # Mensagem de erro
            await ctx.send('A magia não foi encontrada.')
            return

        # Enviar Embeds
        embeds = await self.format_spell(spell)
        for iteration, embed in enumerate(embeds):
            # Verifica se a mensagem precisa de imagem
            if iteration == 0 and spell['tabela']:
                file = self.tables[spell['tabela']-1]
                embed.set_image(url="attachment://" + file.filename)
                await ctx.send(embed=embed, file=file)
                continue
            await ctx.send(embed=embed)

    async def format_spell(self, spell:dict) -> list:
        """
        Formata os textos da magia e retorna como embed.
        
        :param spell: <dict> dados da magia;
        :return embeds_list: <list>
        """
        ritual = ' **(Ritual)**' if spell['ritual'] else ''
        description = spell['descrição'].replace('Em Níveis Superiores.', '**Em Níveis Superiores.**')

        # Adiciona negrito (**) nas frases que tem \t 
        if '\t' in description:
            description = list(spell['descrição'])
            x = False
            for iteration, letter in enumerate(description):
                if j == '\t':
                    description[iteration] = '\t**'
                    x = True
                elif j == '.' and x == True:
                    description[iteration] = '.**'
                    x = False
            description = ''.join(description)

        # Verificar se o texto cabe em um só embed
        if len(description) > 1024:
            description = await text_splitter(description)
        else:
            description = [description]

        # Criação dos embeds
        embeds = []
        for iteration, text in enumerate(description):
            if iteration == 0:
                embed = Embed(
                    title= spell['nome'], 
                    colour= self.colours[spell['escola']],   
                    description= str(spell['nível']) + 'º nível de ' + 
                        spell['escola'] + ritual if spell['nível'] != 0
                        else 'Truque de ' + spell['escola'],
                )
                
                fields = [
                    ('Conjuradores', ', '.join(spell['classes'])),
                    ('Tempo de Conjuração', spell['tempo de conjuração']),
                    ('Alcance', spell['alcance']),
                    ('Componentes', spell['componentes']),
                    ('Duração', spell['duração']),
                    ('Descrição', text)
                ]

                for i in fields:
                    embed.add_field(name=i[0], value=i[1], inline=False)
            else:
                embed = Embed(
                    title= spell['nome'] + ' - Continuação', 
                    colour= self.colours[spell['escola']],   
                    description= text,
                )
            embed.set_footer(text='Fonte: ' + spell['fonte'])
            embeds.append(embed)
        return embeds

async def text_splitter(text:str, for_embed=True) -> list:
    """
    Fragmenta o texto em partes menores dentro do limite máximo
    de caracteres
    
    :param text: str
    :return list:
    """
    splitted = text.split('\n')
    result = []
    for i, part in enumerate(splitted):
        #  Verificar se é o primeiro
        if i == 0:
            # Inicia primeiro bloco de texto
            text = part
            continue
        # Definir o limite de caracteres
        length = 4096   # valor da descrição
        if for_embed:
            if len(result) == 0:
                length = 1024   # valor do field
        # Verificar se já atingiu o limite de caracteres
        if len(text)+1 + len(part) > length:
            result.append(text)
            text = part
        else:
            text += '\n' + part

        # Verificar se é o último
        if i+1 == len(splitted):
            result.append(text)
    return result