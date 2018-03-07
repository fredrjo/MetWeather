import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS stations (id text UNIQUE, name text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS measurements (id INTEGER PRIMARY KEY, mType text, value real)"
cursor.execute(create_table)

connection.commit()

connection.close()