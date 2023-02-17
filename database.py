import sqlite3 as sql

con = sql.connect('database.db')

cur = con.cursor()
with open('schema.sql') as init_script:
    cur.executescript(init_script.read())

con.commit()