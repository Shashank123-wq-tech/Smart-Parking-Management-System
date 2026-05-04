import psycopg2
import os

def get_db_connection():
    db_url = os.environ.get("DATABASE_URL")

    if not db_url:
        raise Exception("DATABASE_URL not set")

    return psycopg2.connect(db_url, sslmode='require')


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS bookings CASCADE;")
    cur.execute("DROP TABLE IF EXISTS slots CASCADE;")
    cur.execute("DROP TABLE IF EXISTS vehicle_types CASCADE;")
    cur.execute("DROP TABLE IF EXISTS users CASCADE;")

    # USERS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT
    )
    """)

    # VEHICLE TYPES (✅ FIXED COLUMN NAME)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS vehicle_types (
        id SERIAL PRIMARY KEY,
        name TEXT,
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

    # INSERT DEFAULT VEHICLES
    cur.execute("SELECT COUNT(*) FROM vehicle_types")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO vehicle_types (name, price_per_hour) VALUES (%s, %s)", ("Car", 50))
        cur.execute("INSERT INTO vehicle_types (name, price_per_hour) VALUES (%s, %s)", ("Bike", 20))
        cur.execute("INSERT INTO vehicle_types (name, price_per_hour) VALUES (%s, %s)", ("Truck", 100))
        cur.execute("INSERT INTO vehicle_types (name, price_per_hour) VALUES (%s, %s)", ("Van", 70))

    # INSERT SLOTS
    cur.execute("SELECT COUNT(*) FROM slots")
    if cur.fetchone()[0] == 0:
        for _ in range(5):
            cur.execute("INSERT INTO slots (vehicle_type_id) VALUES (%s)", (1,))
        for _ in range(5):
            cur.execute("INSERT INTO slots (vehicle_type_id) VALUES (%s)", (2,))

    conn.commit()
    cur.close()
    conn.close()
    