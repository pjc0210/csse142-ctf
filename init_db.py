import sqlite3
import random
import string

DB_NAME = 'users.db'
USER_COUNT = 500

def random_string(length=12):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS users')
    cur.execute('CREATE TABLE users (username TEXT PRIMARY KEY, password TEXT)')

    for _ in range(USER_COUNT):
        username = random_string(8)
        password = random_string(16)
        cur.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))

    conn.commit()
    conn.close()
    print(f"{USER_COUNT} users generated in {DB_NAME}.")

if __name__ == "__main__":
    init_db()
