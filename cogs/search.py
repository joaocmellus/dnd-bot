from os import path, listdir
from json import load

PY_DIR = path.dirname(__file__)

class Search:
    """
    Classe para fazer pesquisas na base de dados.
    """
    def __init__(self, file_name:str):
        """
        :param file_name: <str> nome do arquivo que contém os dados 
        a serem lidos.
        """
        file_data = read(file_name)
        self.data = {}
        for i in file_data:
            self.data[i['nome'].lower()] = i

    async def get_data(self, name:str) -> dict:
        """
        Retorna o conteúdo de um único dado pesquisado pelo nome.

        :param name: <str>
        :return: <dict>
        """
        return self.data.get(name, None)

    async def get_all(self, *keys) -> list:
        """
        Retorna uma lista de todo o contéudo somente com
        os dados das keys passadas como parâmetro.
        
        :param keys: <str> keys que serão pesquisadas
        :return: <list> [tuple(item), tuple(item)]
        """
        return [tuple(v[k] for k in keys) for v in self.data.values()]

def read(file_name:str) -> list:
    """
    Lê um arquivo json e retorna o conteúdo.
    """
    file = path.join(PY_DIR, '..', 'data', file_name)
    with open(file, 'r', encoding='utf-8') as doc:
        return load(doc)

# mudar depois -> ver como essa função interage com o embed
def read_tables() -> list:
    """
    Retorna o path de todas as imagens da pasta 'data/tables'.
    """
    dir_path = path.join(PY_DIR, '..', 'data', 'tables')
    tables = []
    for file in listdir(dir_path): 
        tables.append((path.join(dir_path, file)))
    return tables