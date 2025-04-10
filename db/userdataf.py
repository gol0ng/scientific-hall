import sqlite3

conn = sqlite3.connect('科创广场.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  password TEXT,
                  name TEXT,
                  avatar TEXT,
                  major TEXT,
                  job TEXT,
                  e_mail TEXT,
                  introduction,
                  admin INTEGER DEFAULT 0
                  )''')
conn.commit()
conn.close()

def add_user(username, password, name, avatar, major, job, e_mail, introduction):
    conn = sqlite3.connect('科创广场.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO users (username, password, name, avatar, major, job, e_mail, introduction)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                   (username, password, name, avatar, major, job, e_mail, introduction))
    conn.commit()
    conn.close()

def get_user(username):
    conn = sqlite3.connect('科创广场.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM users WHERE username=?''', (username,))
    user = cursor.fetchone()
    if user:
        conn.close()
        return {
            'id': user[0],
            'username': user[1],
            'password': user[2],
            'name': user[3],
            'avatar': user[4],
            'major': user[5],
            'job': user[6],
            'e_mail': user[7],
            'introduction': user[8],
        }
    else:
        conn.close()
        return None

def get_user_almost(query):# 模糊查找
    conn = sqlite3.connect('科创广场.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM users 
        WHERE name LIKE ? 
        OR major LIKE ? 
        OR introduction LIKE ?
    ''', ('%' + query + '%', '%' + query + '%', '%' + query + '%'))
    users = cursor.fetchall()
    conn.close()
    return [{
        'id': user[0],
        'username': user[1],
        'password': user[2],
        'name': user[3],
        'avatar': user[4],
        'major': user[5],
        'job': user[6],
        'e_mail': user[7],
        'introduction': user[8],
    }for user in users]

def get_user_by_id(id):
    conn = sqlite3.connect('科创广场.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM users WHERE id=?''', (id,))
    user = cursor.fetchone()
    if user:
        conn.close()
        return {
            'id': user[0],
            'username': user[1],
            'password': user[2],
            'name': user[3],
            'avatar': user[4],
            'major': user[5],
            'job': user[6],
            'e_mail': user[7],
            'introduction': user[8],
        }