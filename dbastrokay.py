import sqlite3

def create_database():

    # create the database file and tables
    db_file = "astrophotography.db"
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    # Create tables for each button
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

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def add_data(table, file_info):
    # establish connection to the database
    connection = sqlite3.connect("astrophotography.db")
    cursor = connection.cursor()

    try:
        # insert the file info into the specified table
        cursor.execute(f"INSERT INTO {table} (filename, path) VALUES (?, ?)", file_info)
        connection.commit()
        print("Data added successfully.")
    except sqlite3.Error as e:
        print(f"Error adding data: {e}")
    finally:
        # close the database connection
        connection.close()



def get_data(table_name):
    """
    Returns all the data in the given table.

    Args:
    - table_name (str): name of the table to fetch data from.

    Returns:
    - data (list): list of tuples containing the data.
    """
    conn = sqlite3.connect("astrophotography.db")
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table_name}")
    data = cur.fetchall()
    conn.close()
    return data


connection = sqlite3.connect("astrophotography.db")
cursor = connection.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print(cursor.fetchall())

cursor.execute("PRAGMA table_info(FlatFrame)")
print(cursor.fetchall())

connection.close()