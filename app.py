from flask import Flask, render_template, request, redirect, session
from datetime import datetime
from models import get_db_connection, init_db

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Initialize DB
init_db()


# ---------------- HOME ----------------
@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM vehicle_types")
    vehicle_types = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('index.html', vehicle_types=vehicle_types)


# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()

        # ✅ Check duplicate email
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing = cur.fetchone()

        if existing:
            cur.close()
            conn.close()
            return "❌ Email already exists"

        cur.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, password)
        )

        conn.commit()
        cur.close()
        conn.close()

        return redirect('/login')

    return render_template('register.html')


# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE email = %s AND password = %s",
            (email, password)
        )

        user = cur.fetchone()

        cur.close()
        conn.close()

        if user:
            session['user_id'] = user[0]   # id is index 0
            return redirect('/')
        else:
            return "❌ Invalid credentials"

    return render_template('login.html')


# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# ---------------- BOOK SLOT ----------------
@app.route('/book', methods=['POST'])
def book():

    if 'user_id' not in session:
        return redirect('/login')

    vehicle_type = int(request.form['vehicle_type'])
    start_time = request.form['start_time']
    end_time = request.form['end_time']

    conn = get_db_connection()
    cur = conn.cursor()

    # 🔥 Check available slot (no conflict)
    cur.execute("""
    SELECT * FROM slots 
    WHERE vehicle_type_id = %s
    AND id NOT IN (
        SELECT slot_id FROM bookings
        WHERE (start_time < %s AND end_time > %s)
    )
    LIMIT 1
    """, (vehicle_type, end_time, start_time))

    slot = cur.fetchone()

    if not slot:
        cur.close()
        conn.close()
        return "❌ No parking available for this time slot"

    slot_id = slot[0]

    # 🧮 Calculate duration
    fmt = "%Y-%m-%dT%H:%M"
    start = datetime.strptime(start_time, fmt)
    end = datetime.strptime(end_time, fmt)

    hours = (end - start).total_seconds() / 3600

    if hours <= 0:
        return "❌ Invalid time selection"

    # 💰 Get price
    cur.execute(
        "SELECT price_per_hour FROM vehicle_types WHERE id = %s",
        (vehicle_type,)
    )
    price = cur.fetchone()[0]

    total_amount = hours * price

    # 💾 Insert booking
    cur.execute("""
    INSERT INTO bookings 
    (user_id, slot_id, start_time, end_time, total_amount, status)
    VALUES (%s, %s, %s, %s, %s, %s)
    """, (session['user_id'], slot_id, start, end, total_amount, 'booked'))

    conn.commit()
    cur.close()
    conn.close()

    return redirect('/my_bookings')


# ---------------- VIEW BOOKINGS ----------------
@app.route('/my_bookings')
def my_bookings():

    if 'user_id' not in session:
        return redirect('/login')

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT b.id, b.start_time, b.end_time, b.total_amount, s.id
    FROM bookings b
    JOIN slots s ON b.slot_id = s.id
    WHERE b.user_id = %s
    ORDER BY b.start_time DESC
    """, (session['user_id'],))

    data = cur.fetchall()

    cur.close()
    conn.close()

    bookings_list = []

    for b in data:
        bookings_list.append({
            "id": b[0],
            "slot_id": b[4],
            "start_time": b[1],
            "end_time": b[2],
            "total_amount": b[3],
            "status": "Completed" if b[2] < datetime.now() else "Active"
        })

    return render_template('bookings.html', bookings=bookings_list)


# ---------------- CANCEL ----------------
@app.route('/cancel/<int:booking_id>')
def cancel_booking(booking_id):

    if 'user_id' not in session:
        return redirect('/login')

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
    UPDATE bookings 
    SET status = 'cancelled'
    WHERE id = %s AND user_id = %s
    """, (booking_id, session['user_id']))

    conn.commit()
    cur.close()
    conn.close()

    return redirect('/my_bookings')


# ---------------- ADMIN ----------------
@app.route('/admin')
def admin_dashboard():

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM bookings")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM bookings WHERE status='booked'")
    active = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM bookings WHERE status='cancelled'")
    cancelled = cur.fetchone()[0]

    cur.close()
    conn.close()

    return render_template('admin.html',
                           total=total,
                           active=active,
                           cancelled=cancelled)


# ---------------- SLOTS ----------------
@app.route('/slots')
def view_slots():

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT s.id, s.vehicle_type_id,
    CASE 
        WHEN s.id IN (SELECT slot_id FROM bookings WHERE status='booked')
        THEN 'Occupied'
        ELSE 'Available'
    END
    FROM slots s
    """)

    slots = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('slots.html', slots=slots)


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)