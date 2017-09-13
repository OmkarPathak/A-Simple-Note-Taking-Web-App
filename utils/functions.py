import os
import hashlib


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
    '''
        Checks whether a user exists with the specified username and password
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        result = cursor.fetchone()
        if result:
            return result[0]
    except:
        return False


def check_username(username):
    '''
        Checks whether a username is already taken or not
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username=?', (username, ))
        if cursor.fetchone():
            return True
    except:
        return False


def signup_user(username, password, email):
    '''
        Function for storing the details of a user into the database
        while registering
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users(username, password, email) VALUES (?, ?, ?)", (username, password, email))
        conn.commit()
        cursor.close()
        return
    except:
        cursor.close()


def get_data_using_user_id(id):
    '''
        Function for getting the data of a specific user using his user_id
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM notes WHERE user_id=' + str(id))
        results = cursor.fetchall()
        cursor.close()
        return results
    except:
        cursor.close()


def get_data_using_id(id):
    '''
        Function for retrieving data of a specific note using its id
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM notes WHERE id=' + str(id))
        results = cursor.fetchall()
        cursor.close()
        return results
    except:
        cursor.close()


def get_data():
    '''
        Function for getting data of all notes
    '''
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM notes')
    results = cursor.fetchall()
    cursor.close()
    return results


def add_note(note_title, note, note_markdown, user_id):
    '''
        Function for adding note into the database
    '''
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes(note_title, note, note_markdown, user_id) VALUES (?, ?, ?, ?)", (note_title, note, note_markdown, user_id))
    conn.commit()
    cursor.close()
    return


def edit_note(note_title, note, note_markdown, user_id):
    '''
        Function for adding note into the database
    '''
    conn = get_database_connection()
    cursor = conn.cursor()
    print("UPDATE notes SET note_title=?, note=?, note_markdown=? WHERE user_id=?", (note_title, note, note_markdown, user_id))
    cursor.execute("UPDATE notes SET note_title=?, note=?, note_markdown=? WHERE user_id=?", (note_title, note, note_markdown, user_id))
    conn.commit()
    cursor.close()
    return


def delete_note_using_id(id):
    '''
        Function for deleting a specific note using its id
    '''
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id=" + str(id))
    conn.commit()
    cursor.close()
    return


def generate_password_hash(password):
    hashed_value = hashlib.md5(password.encode())
    return hashed_value.hexdigest()

# def dummy_data():
#     conn = get_database_connection()
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO notes(note_title, note) VALUES (?, ?)", ('First', 'Yoo First Note'))
#     conn.commit()
#     cursor.close()


# def select_data():
#     conn = get_database_connection()
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM notes')
#     print(cursor.fetchall())
#     cursor.close()


# if __name__ == '__main__':
#     # dummy_data()
#     # signup_user('omkarpathak27', '8149omkar', 'omkarpathak27@gmail.com')
#     select_data()
#     # print(get_data_using_id(1))
