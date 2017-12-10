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


def get_user_count():
    '''
        Checks whether a user exists with the specified username and password
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM users')
        result = cursor.fetchone()
        if result:
            return result[0]
    except:
        return False


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


def store_last_login(user_id):
    '''
        Checks whether a user exists with the specified username and password
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET last_login=(strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')) WHERE id=?", (user_id, ))
        conn.commit()
        cursor.close()
    except:
        cursor.close()


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


def get_user_data(user_id):
    '''
        Function for getting the data of a specific user using his user_id
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id=?', (str(user_id), ))
        results = cursor.fetchall()
        cursor.close()
        if len(results) == 0:
            return None
        return results
    except:
        cursor.close()


def get_data_using_user_id(id):
    '''
        Function for getting the data of all notes using user_id
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM notes WHERE user_id=' + str(id))
        results = cursor.fetchall()
        cursor.close()
        if len(results) == 0:
            return None
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


def get_number_of_notes(id):
    '''
        Function for retrieving number of notes stored by a specific user
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(note) FROM notes WHERE user_id=' + str(id))
        results = cursor.fetchone()[0]
        cursor.close()
        return results
    except:
        cursor.close()


def get_data():
    '''
        Function for getting data of all notes
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM notes')
        results = cursor.fetchall()
        cursor.close()
        return results
    except:
        cursor.close()


def add_note(note_title, note, note_markdown, tags, user_id):
    '''
        Function for adding note into the database
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO notes(note_title, note, note_markdown, tags, user_id) VALUES (?, ?, ?, ?, ?)", (note_title, note, note_markdown, tags, user_id))
        conn.commit()
        cursor.close()
        return
    except:
        cursor.close()


def edit_note(note_title, note, note_markdown, tags, note_id):
    '''
        Function for adding note into the database
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        # print("UPDATE notes SET note_title=?, note=?, note_markdown=?, tags=? WHERE id=?", (note_title, note, note_markdown, tags, note_id))
        cursor.execute("UPDATE notes SET note_title=?, note=?, note_markdown=?, tags=? WHERE id=?", (note_title, note, note_markdown, tags, note_id))
        conn.commit()
        cursor.close()
        return
    except:
        cursor.close()


def delete_note_using_id(id):
    '''
        Function for deleting a specific note using its id
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM notes WHERE id=" + str(id))
        conn.commit()
        cursor.close()
        return
    except:
        cursor.close()


def generate_password_hash(password):
    '''
        Function for generating a password hash
    '''
    hashed_value = hashlib.md5(password.encode())
    return hashed_value.hexdigest()


def add_tag(tag, user_id):
    '''
        Function for adding a tag into the database
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tags(tag, user_id) VALUES (?, ?)", (tag, user_id))
        conn.commit()
        cursor.close()
        return
    except:
        cursor.close()


def get_all_tags(user_id):
    '''
        Function for getting all tags for a specific user
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT id, tag FROM tags WHERE user_id=?', (str(user_id), ))
        results = cursor.fetchall()
        if len(results) > 0:
            results = [(str(results[i][0]), results[i][1]) for i in range(len(results))]
        else:
            results = None
        cursor.close()
        return results
    except:
        cursor.close()


def get_data_using_tag_id(tag_id):
    '''
        Function for getting all tags for a specific user
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT tag FROM tags WHERE id=?', (str(tag_id), ))
        results = cursor.fetchone()
        cursor.close()
        return results
    except:
        cursor.close()


def get_tag_using_note_id(id):
    '''
        Get the tags associated with each note
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT tags FROM notes WHERE id=?', (str(id), ))
        results = cursor.fetchall()
        # results = [(str(results[i][0]), results[i][1]) for i in range(len(results))]
        results = results[0][0].split(',')
        cursor.close()
        return results
    except:
        cursor.close()


def get_tagname_using_tag_id(tag_id):
    '''
        Get the tag name using tag id
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT tag FROM tags WHERE id=?', (str(tag_id), ))
        results = cursor.fetchone()
        cursor.close()
        return ''.join(results)
    except:
        cursor.close()


def delete_tag_using_id(tag_id):
    '''
        Function for deleting a specific tag using its id
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tags WHERE id=" + str(tag_id))
        conn.commit()
        cursor.close()
        return
    except:
        cursor.close()


def get_number_of_tags(id):
    '''
        Function for retrieving number of tags stored by a specific user
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(tag) FROM tags WHERE user_id=' + str(id))
        results = cursor.fetchone()[0]
        cursor.close()
        return results
    except:
        cursor.close()


def get_notes_using_tag_id(tag_id, username):
    '''
        Function for retrieving notes stored by a specific tag
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT id, note_title FROM notes WHERE user_id=? AND tags like ?', (username, '%' + tag_id + '%'))
        results = cursor.fetchall()
        cursor.close()
        return results
    except:
        cursor.close()


def edit_email(email, user_id):
    '''
        Function for adding note into the database
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET email=? WHERE id=?", (email, user_id))
        conn.commit()
        cursor.close()
        return
    except:
        cursor.close()


def edit_password(password, user_id):
    '''
        Function for adding note into the database
    '''
    conn = get_database_connection()
    password = generate_password_hash(password)
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET password=? WHERE id=?", (password, user_id))
        conn.commit()
        cursor.close()
        return
    except:
        cursor.close()


def get_search_data(pattern, user_id):
    '''
        Function for searching note based on specified pattern
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM notes WHERE user_id=? AND note_title LIKE ? LIMIT 3", (user_id, '%' + pattern + '%'))
        results = cursor.fetchall()
        results = [(results[i][0], results[i][3]) for i in range(len(results))]
        cursor.close()
        return results
    except:
        cursor.close()


def get_rest_data_using_user_id(id):
    '''
        Function for getting the data of all notes using user_id using REST
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM notes WHERE user_id=' + str(id))
        results = cursor.fetchall()
        fieldnames = [f[0] for f in cursor.description]
        cursor.close()
        if len(results) == 0:
            return None
        else:
            outer = {}
            for i in range(len(results)):
                data = {}
                for j in range(len(results[0])):
                    data[fieldnames[j]] = results[i][j]
                outer[int(i)] = data

            return outer
    except:
        cursor.close()


# if __name__ == '__main__':
    # print(get_rest_data_using_user_id(1))
    # print(get_data_using_id(1))
