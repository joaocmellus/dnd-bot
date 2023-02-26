from os import path, listdir
from json import load

class DataQuery:
    """
    Uma classe para representar uma base de dados e prover meios de acesso.

    Atributos:
        data <dict>: A base de dados em si, um dicionário de dicionários
            ordenados pela chave passada como parâmetro.
            Ex:
                data = {
                    <id 1> = <dado 1>,
                    <id 2> = <dado 2>
                }
            Sendo <id> o valor presente em <dado[id]>

    Métodos:
        get(name): Retorna um dicionário ou None.
        all(*keys): Retorna uma lista de todos os dados com tuplas contendo 
            apenas com os dados referêntes às keys passadas como parâmetro.
    """
    def __init__(self, data, index_key=None):
        """
        :param data: <list or dict> base de dados.
        :param index_key: <str> key que será usada como identificador caso
        a base de dados seja uma lista.
        """
        assert data, 'A base de dados está vazia.'
        if type(data) == list:
            assert index_key, 'A key identificadora não pode ser um <NoneType>'
            self.data = {}
            for i in data:
                self.data[i[index_key].lower()] = i
        else:
            self.data = data

    async def get(self, name:str) -> dict:
        """
        Retorna o conteúdo de um único dado pesquisado pelo valor passado 
        como chave.

        :param name: <str> key identificadora usada como identificador.

        :return: <dict>
        """
        return self.data.get(name.lower(), None)

    async def all(self, *keys) -> list:
        """
        Retorna uma lista de todo o contéudo somente com os dados das
        respectivas keys passadas como parâmetro.
        
        :param keys: <str> keys que serão pesquisadas
        """
        return [tuple(v[k] for k in keys) for v in self.data.values()]

class DataRepository:
    """
    Uma classe para agrupar diferentes tipos de bases de dados em formato
    'json' que possuem relação.
    
    Atributos:
        files <list>: uma lista com todos os arquivos que foram incorporados
            à classe.
        
        *<'file_name'> <DataQuery>: dados incorporados do arquivos, são acessados 
            pelo nome respectivo do arquivo.

    Métodos:
        add(file_path, key): recebe o path de um json e incorpora seu conteúdo
            à classe.
        add_dir(dir_path, commom_key): recebe o path de um diretório e incorpora
            o conteúdo de todos os jsons nele à classe.
    """
    def __init__(self):
        self.files = []

    def __str__(self):
        text = 'DataRepository:'
        for v in self.files:
            text += '\n| ' + v
        return text

    def add(self, file_path, key=None) -> None:
        """
        Lê os dados de um novo arquivo json ao repositório.

       :param file_path: <str> path do arquivo.
       :param key: <str> key do dado que contém a chave identificadora
       dos dados.
        """
        with open(file_path, 'r', encoding='utf-8') as doc:
            data = load(doc)
        filename = path.basename(file_path)
        setattr(self, filename[:-5], DataQuery(data, key))
        self.files.append(filename)

    def add_dir(self, dir_path, commom_key=None) -> None:
        """
        Lê todos os dados de um diretório.

        :param dir_path: <str> path do diretório
        :param common_key: <str> chave dos dados que contém a chave 
        identificadora dos dados (ela tem que ser estar presente em todos 
        os arquivos de dados do diretório).
        """
        for file in listdir(dir_path):
            if file.endswith('.json'):
                file_path = path.join(dir_path, file)
                self.add(file_path, commom_key)

def read_tables() -> list:
    """
    Retorna o path de todas as imagens da pasta 'data/tables'.
    """
    dir_path = path.join('data', 'tables')
    tables = []
    for file in listdir(dir_path): 
        tables.append((path.join(dir_path, file)))
    return tables