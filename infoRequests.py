import sqlite3

# Classe estática para fazer a conexão com o db
class DB:
	file = 'Database/database.db'

	async def connect():
		db = sqlite3.connect(DB.file)
		cursor = db.cursor()
		return db, cursor

# Requisões relacionadas com magias
class SpellRequests:

	async def get_spell(spell_name:str) -> list:
		'''Retorna as informações de uma magia em uma lista:
		(id, nome, nível, ritual, escola, tempo de conjuração, alcance, componentes, duração, descrição, tabela, fonte, classes)'''
		db, cursor = await DB.connect()
		# Pegar informações da magia
		sql = '''SELECT Spell.id, Spell.name, level, ritual, school, casting_time, range, components, duration, description, has_table, Book.name 
				FROM Spell 
				INNER JOIN Book
				ON Spell.source = Book.id 
				WHERE Spell.name LIKE ?;'''
		cursor.execute(sql, [spell_name])

		# Verifica se há alguma magia
		try:
			result = list(cursor.fetchall()[0])
		except IndexError:
			return False
		
		# Pegar classes relacionadas à magia
		sql = '''SELECT Class.name
				FROM Class
				INNER JOIN Spell, SpellReference
				ON SpellReference.spell_id = Spell.id AND SpellReference.class_id = Class.id
				WHERE Spell.id = ?;'''
		cursor.execute(sql, [result[0]])
		classes = [i[0] for i in cursor.fetchall()]
		result.append(classes)
		db.close()
		return result

	async def get_class():
		pass