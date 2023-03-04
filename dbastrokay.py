import sqlite3

def create_database():
    db_file = "astrophotography.db"
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS FlatFrame
            (filename TEXT, path TEXT)''')
    conn.commit()
    conn.close()

def add_data(table, file_info):
    connection = sqlite3.connect("astrophotography.db")
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO {table} (filename, path) VALUES (?, ?)", file_info)
    connection.commit()
    connection.close()

