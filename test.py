import sqlite3 as sql

con = sql.connect('database.db')

cur = con.cursor()
cur.execute("""CREATE TABLE user_cities(
            chat_id INTEGER PRIMARY KEY,
            city TEXT NOT NULL)
            """)