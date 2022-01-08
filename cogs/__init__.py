from os import path, listdir
from json import load

pyDir = path.dirname(__file__)

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