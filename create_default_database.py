import sqlite3
import json

db = sqlite3.connect('Database/database.db')
cursor = db.cursor()

# Criar tabelas
cursor.execute('''CREATE TABLE Class (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(25) NOT NULL
);'''
)

cursor.execute('''CREATE TABLE Book(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(50) NOT NULL
);'''
)

cursor.execute('''CREATE TABLE Spell(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(100) NOT NULL,
	level INTEGER(1) NOT NULL,
	ritual INTEGER(1) NOT NULL,
	school VARCHAR(20) NOT NULL,
	casting_time TEXT NOT NULL,
	range TEXT NOT NULL,
	components TEXT NOT NULL,
	duration TEXT NOT NULL,
	description TEXT NOT NULL,
	has_table INTEGER(1) NOT NULL,
	source INTEGER NOT NULL,
	FOREIGN KEY (source) REFERENCES Book(id)
);'''
)

cursor.execute('''CREATE TABLE SpellReference(
	spell_id INTEGER NOT NULL,
	class_id INTEGER NOT NULL,
	FOREIGN KEY (spell_id) REFERENCES Spell(id),
	FOREIGN KEY (class_id) REFERENCES Class(id)
);'''
)

with open('JsonData/magias.json', 'r', encoding='utf-8') as arq:
	# lista com dicionários das magias
	magias = json.load(arq)

with open('JsonData/magiasClasse.json', 'r', encoding='utf-8') as arq:
	magiasClasse = json.load(arq)

# colocar livros no banco
livros = []
for magia in magias:
	if magia['fonte'] not in livros:
		livros.append(magia['fonte'])
livros.sort()
for i in livros:
	cursor.execute('''INSERT INTO Book VALUES (NULL, ?)''', ([i]))

# colocar classes no banco
classes = []
for classe in magiasClasse:
	if classe not in classes:
		classes.append(classe)
classes.sort()
for i in classes:
	cursor.execute('''INSERT INTO Class VALUES (NULL, ?)''', ([i]))

# colocar magias no banco
for magia in magias:
	fonte = livros.index(magia['fonte']) + 1
	cursor.execute('''INSERT INTO Spell VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', ([magia['nome'], 
		magia['nível'], magia['ritual'], magia['escola'], magia['tempo de conjuração'], magia['alcance'],
		magia['componentes'], magia['duração'], magia['descrição'], magia['tabela'], fonte]))

# colocar referencias o.o
for magia in magias:
	# Magia Id
	cursor.execute('''SELECT id FROM Spell WHERE name = ?;''', [magia['nome']])
	magia_id = cursor.fetchall()[0][0]

	# Class Id
	for classe in magia['classes']:
		classe_id = classes.index(classe) + 1
		cursor.execute('''INSERT INTO SpellReference VALUES (?, ?)''', ([magia_id, classe_id]))

db.commit()
db.close()