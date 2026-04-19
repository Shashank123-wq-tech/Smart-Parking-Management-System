from models import get_db_connection, init_db
import sqlite3
init_db()

conn = get_db_connection()

# vehicle types
conn.execute("INSERT INTO vehicle_types (type_name, price_per_hour) VALUES ('Car', 50)")
conn.execute("INSERT INTO vehicle_types (type_name, price_per_hour) VALUES ('Bike', 20)")
conn.execute("INSERT INTO vehicle_types (type_name, price_per_hour) VALUES ('Truck', 100)")
conn.execute("INSERT INTO vehicle_types (type_name, price_per_hour) VALUES ('Van', 70)")

# slots
for i in range(5):
    conn.execute("INSERT INTO slots (vehicle_type_id) VALUES (1)")

for i in range(5):
    conn.execute("INSERT INTO slots (vehicle_type_id) VALUES (2)")

conn.commit()
conn.close()

print("Data inserted successfully!")