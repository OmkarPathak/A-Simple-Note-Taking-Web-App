import os


def get_database_connection():
    '''
        Creates a connection between selected database
    '''
    import sqlite3
    sqlite_file = 'notes.db'
    file_exists = os.path.isfile(sqlite_file)
    conn = sqlite3.connect(sqlite_file)
    if not file_exists:
        create_sqlite_tables(conn)
    return conn


def create_sqlite_tables(conn):
    '''
        Creates a sqlite table as specified in schema_sqlite.sql file
    '''
    cursor = conn.cursor()
    with open('schema_sqlite.sql', 'r') as schema_file:
        cursor.executescript(schema_file.read())
    conn.commit()


def check_user_exists(username, password):
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        if cursor.fetchone():
            return True
    except:
        return False


def check_username(username):
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username=?', (username, ))
        if cursor.fetchone():
            return True
    except:
        return False


def signup_user(username, password, email):
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users(username, password, email) VALUES (?, ?, ?)", (username, password, email))
        conn.commit()
        cursor.close()
        return
    except:
        cursor.close()
        print('Something went wrong!')


# def dummy_data():
#     conn = get_database_connection()
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO users(username, password) VALUES (?, ?)", ('omkarpathak', '8149omkar'))
#     conn.commit()
#     cursor.close()


# def select_data():
#     conn = get_database_connection()
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM users')
#     print(cursor.fetchall())
#     cursor.close()


# if __name__ == '__main__':
#     # dummy_data()
#     signup_user('omkarpathak27', '8149omkar', 'omkarpathak27@gmail.com')
#     select_data()

