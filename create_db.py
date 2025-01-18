import sqlite3 

# открываем файл с базой данных
con = sqlite3.connect('history_db.db')

# создаём таблицу 
with con:
    con.execute("""
        CREATE TABLE history (
            id INTEGER PRIMARY KEY,
            text TEXT,
            date DATE,
            chat_id VARCHAR(20),
            user_id VARCHAR(20)
);
    """)