import sqlite3

def create_database():


    db_file = "astrophotography.db"
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS LightFrame
            (filename TEXT, path TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS DarkFrame
            (filename TEXT, path TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS FlatFrame
            (filename TEXT, path TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS DarkFlatFrame
            (filename TEXT, path TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS BiasFrame
            (filename TEXT, path TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS YourFrame
            (filename TEXT, path TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS MasterDarkFlat
            (filename TEXT, path TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS MasterDark
            (filename TEXT, path TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS MasterFlat
            (filename TEXT, path TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS MasterBias
            (filename TEXT, path TEXT)''')


    conn.commit()
    conn.close()


def add_data(table, file_info):

    connection = sqlite3.connect("astrophotography.db")
    cursor = connection.cursor()

    try:

        cursor.execute(f"INSERT INTO {table} (filename, path) VALUES (?, ?)", file_info)
        connection.commit()
        print("Data added successfully.")
    except sqlite3.Error as e:
        print(f"Error adding data: {e}")
    finally:

        connection.close()



def get_data(table_name):

    conn = sqlite3.connect("astrophotography.db")
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table_name}")
    data = cur.fetchall()
    conn.close()
    return data
