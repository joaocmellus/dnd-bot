from os import path, listdir
from json import load

pyDir = path.dirname(__file__)

class Search:
	def __init__(self, file_name):
		self.data = {i['nome'].lower() : i for i in read(file_name)}

	async def get_data(self, name):
		name = name.lower()
		return self.data.get(name, None)

	async def get_all(self, *args):
		return [tuple(v[k] for k in args) for v in self.data.values()]

def read(file_name):
	filePath = '..//data//' + file_name
	file = path.join(pyDir, filePath)
	with open(file, 'r', encoding='utf-8') as doc:
		return load(doc)

def read_tables() -> list:
	dirPath = '..//data//tables//'
	files = []
	for file in listdir(path.join(pyDir, dirPath)): 
		filePath = path.join(pyDir, dirPath + file)
		files.append((file, filePath))
	return files