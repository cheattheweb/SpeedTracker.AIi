import sqlite3
from sqlite3 import Error


def create_connection():
    conn = None;
    try:
        conn = sqlite3.connect('database.db') # creates a memory-based database for demonstration. Replace with your database filename.
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn):
    try:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE SpeedingEvents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                time TEXT NOT NULL,
                speed_limit_crossed INTEGER NOT NULL,
                v_id TEXT NOT NULL,
                image BLOB NOT NULL
            )
        """)
    except Error as e:
        print(e)

def insert_data(conn, data):
    try:
        c = conn.cursor()
        c.execute("""
            INSERT INTO SpeedingEvents(time, speed_limit_crossed, v_id, image) VALUES(?,?,?,?)
        """, data)
        conn.commit()
        print("Data inserted successfully")
    except Error as e:
        print("Error inserting data")
        print(e)


