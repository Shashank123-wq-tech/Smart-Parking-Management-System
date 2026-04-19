import sqlite3
from config import Config

def get_db_connection():
    conn = sqlite3.connect(Config.DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()

    # users
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT
    )''')

    # vehicle types
    conn.execute('''CREATE TABLE IF NOT EXISTS vehicle_types (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type_name TEXT,
        price_per_hour INTEGER
    )''')

    # slots
    conn.execute('''CREATE TABLE IF NOT EXISTS slots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicle_type_id INTEGER
    )''')

    # bookings
    conn.execute('''CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        slot_id INTEGER,
        start_time TEXT,
        end_time TEXT,
        total_amount REAL,
        status TEXT
    )''')

    conn.commit()
    conn.close() 
    