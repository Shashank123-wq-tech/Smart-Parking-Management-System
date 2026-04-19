import psycopg2
import os

def get_db_connection():
    db_url = os.environ.get("DATABASE_URL")

    if not db_url:
        raise Exception("DATABASE_URL not set")

    return psycopg2.connect(db_url)


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    # USERS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT
    )
    """)

    # VEHICLE TYPES
    cur.execute("""
    CREATE TABLE IF NOT EXISTS vehicle_types (
        id SERIAL PRIMARY KEY,
        type_name TEXT,
        price_per_hour INTEGER
    )
    """)

    # SLOTS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS slots (
        id SERIAL PRIMARY KEY,
        vehicle_type_id INTEGER REFERENCES vehicle_types(id)
    )
    """)

    # BOOKINGS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        slot_id INTEGER REFERENCES slots(id),
        start_time TIMESTAMP,
        end_time TIMESTAMP,
        total_amount REAL,
        status TEXT
    )
    """)

    # 🔥 INSERT DEFAULT DATA
    cur.execute("SELECT COUNT(*) FROM vehicle_types")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO vehicle_types VALUES (DEFAULT, %s, %s)", ("Car", 50))
        cur.execute("INSERT INTO vehicle_types VALUES (DEFAULT, %s, %s)", ("Bike", 20))
        cur.execute("INSERT INTO vehicle_types VALUES (DEFAULT, %s, %s)", ("Truck", 100))
        cur.execute("INSERT INTO vehicle_types VALUES (DEFAULT, %s, %s)", ("Van", 70))

    cur.execute("SELECT COUNT(*) FROM slots")
    if cur.fetchone()[0] == 0:
        for _ in range(5):
            cur.execute("INSERT INTO slots (vehicle_type_id) VALUES (%s)", (1,))
        for _ in range(5):
            cur.execute("INSERT INTO slots (vehicle_type_id) VALUES (%s)", (2,))

    conn.commit()
    cur.close()
    conn.close()