import sqlite3
from datetime import datetime

# create DB it not already exists
def create_db():
    conn = sqlite3.connect('password_manager.db')
    c = conn.cursor()
    # create table if doesn't exist
    c.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY,
            service TEXT,
            username TEXT,
            password TEXT,
            date_created TEXT,
            last_updated TEXT
        )
    """)
    conn.commit()
    return conn, c

# creates user/pass entry
def create_entry(service, username, password):
    conn, c = create_db()
    date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    last_updated = date_created
    # change this to an fstring
    c.execute('''
        INSERT INTO accounts (service, username, password, date_created, last_updated)
        VALUES (?, ?, ?, ?, ?)
    ''', (service, username, password, date_created, last_updated))
    conn.commit()
    conn.close()


# get all enteries (display)
def get_all_enteries():
    conn, c = create_db()
    # select all
    c.execute('SELECT * FROM accounts')    
    # THIS IS RETURNING TUPLES!
    rows = c.fetchall()
    conn.close()
    return rows


# update service password that exists in DB
def update_entry(password,service_name):
    conn, c = create_db()
    time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('''UPDATE accounts
                  SET password = ?, last_updated = ?
                  WHERE service = ? ''', (password,time_stamp,service_name))
    conn.commit()
    conn.close()




