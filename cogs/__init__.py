from os import path
from json import load

pyDir = path.dirname(__file__)

def read(file_name):
	filePath = '..//data//' + file_name
	file = path.join(pyDir, filePath)
	with open(file, 'r', encoding='utf-8') as doc:
		return load(doc)