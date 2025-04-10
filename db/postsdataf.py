import sqlite3
from datetime import datetime
import pytz

def now():
    # 使用 pytz 获取特定时区的时间
    shanghai_tz = pytz.timezone('Asia/Shanghai')
    shanghai_time = datetime.now(shanghai_tz)
    return str(shanghai_time)[:-16]
conn = sqlite3.connect('科创广场.db')
cursor = conn.cursor()
conn.execute("PRAGMA foreign_keys = ON")
cursor.execute('''CREATE TABLE IF NOT EXISTS posts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT,
                  content TEXT,
                  author TEXT,
                  created_at TEXT,
                  FOREIGN KEY (author) REFERENCES users(id))''')
conn.commit()
conn.close()

def add_post(title, content, author):
    conn = sqlite3.connect('科创广场.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO posts (title, content, author, created_at)
                    VALUES (?, ?, ?, ?)''',
                   (title, content, author, now()))
    conn.commit()
    conn.close()

def get_all_posts():
    conn = sqlite3.connect('科创广场.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM posts''')
    posts = cursor.fetchall()
    conn.close()
    return [{
        'id': post[0],
        'title': post[1],
        'content': post[2],
        'author': post[3],
        'created_at': post[4],
    }for post in posts]

def get_post(post_id):
    conn = sqlite3.connect('科创广场.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM posts WHERE id=?''', (post_id,))
    post = cursor.fetchone()
    conn.close()
    if post:
        return {
            'id': post[0],
            'title': post[1],
            'content': post[2],
            'author': post[3],
            'created_at': post[4],
        }
    return None