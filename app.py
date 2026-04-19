from flask import Flask, render_template, request, redirect, session
from datetime import datetime
from models import get_db_connection, init_db
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret123"

# Initialize database (creates tables)
init_db()


# ---------------- HOME ----------------
@app.route('/')
def index():
    conn = get_db_connection()

    # ✅ THIS IS THE LINE YOU ASKED ABOUT
    vehicle_types = conn.execute("SELECT * FROM vehicle_types").fetchall()

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
        conn.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, password)
        )
        conn.commit()
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
        user = conn.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        ).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
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

    vehicle_type = request.form['vehicle_type']
    start_time = request.form['start_time']
    end_time = request.form['end_time']

    conn = get_db_connection()

    # 🔥 CHECK AVAILABLE SLOT (NO TIME CONFLICT)
    slot = conn.execute("""
    SELECT * FROM slots 
    WHERE vehicle_type_id = ?
    AND id NOT IN (
        SELECT slot_id FROM bookings
        WHERE (start_time < ? AND end_time > ?)
    )
    LIMIT 1
    """, (vehicle_type, end_time, start_time)).fetchone()

    if not slot:
        return "❌ No parking available for this time slot"

    # 🧮 Calculate duration
    fmt = "%Y-%m-%dT%H:%M"
    start = datetime.strptime(start_time, fmt)
    end = datetime.strptime(end_time, fmt)

    hours = (end - start).seconds / 3600

    if hours <= 0:
        return "❌ Invalid time selection"

    # 💰 Get price per hour
    price = conn.execute(
        "SELECT price_per_hour FROM vehicle_types WHERE id=?",
        (vehicle_type,)
    ).fetchone()[0]

    total_amount = hours * price

    # 💾 Insert booking
    conn.execute("""
    INSERT INTO bookings 
    (user_id, slot_id, start_time, end_time, total_amount, status)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (session['user_id'], slot['id'], start_time, end_time, total_amount, 'booked'))

    conn.commit()
    conn.close()

    return f"✅ Booking Successful! Slot {slot['id']} | Amount: ₹{total_amount}"


# ---------------- VIEW BOOKINGS ----------------
@app.route('/my_bookings')
def my_bookings():

    # 🔒 Ensure user is logged in
    if 'user_id' not in session:
        return redirect('/login')

    conn = get_db_connection()

    # 📥 Fetch bookings for logged-in user only
    bookings = conn.execute("""
    SELECT b.id, b.start_time, b.end_time, b.total_amount, s.id as slot_id
    FROM bookings b
    JOIN slots s ON b.slot_id = s.id
    WHERE b.user_id = ?
    ORDER BY b.start_time DESC
    """, (session['user_id'],)).fetchall()

    conn.close()

    # 🔄 Convert and calculate status
    bookings_list = []

    for b in bookings:
        start = datetime.strptime(b['start_time'], "%Y-%m-%dT%H:%M")
        end = datetime.strptime(b['end_time'], "%Y-%m-%dT%H:%M")

        bookings_list.append({
            "id": b['id'],
            "slot_id": b['slot_id'],
            "start_time": b['start_time'],
            "end_time": b['end_time'],
            "total_amount": b['total_amount'],
            "status": "Completed" if end < datetime.now() else "Active"
        })

    return render_template('bookings.html', bookings=bookings_list)

@app.route('/cancel/<int:booking_id>')
def cancel_booking(booking_id):

    if 'user_id' not in session:
        return redirect('/login')

    conn = get_db_connection()

    conn.execute("""
    UPDATE bookings 
    SET status = 'cancelled'
    WHERE id = ? AND user_id = ?
    """, (booking_id, session['user_id']))

    conn.commit()
    conn.close()

    return redirect('/my_bookings')

@app.route('/admin')
def admin_dashboard():

    conn = get_db_connection()

    total_bookings = conn.execute("SELECT COUNT(*) FROM bookings").fetchone()[0]
    active = conn.execute("SELECT COUNT(*) FROM bookings WHERE status='booked'").fetchone()[0]
    cancelled = conn.execute("SELECT COUNT(*) FROM bookings WHERE status='cancelled'").fetchone()[0]

    conn.close()

    return render_template('admin.html',
                           total=total_bookings,
                           active=active,
                           cancelled=cancelled)
    
@app.route('/slots')
def view_slots():

    conn = get_db_connection()

    slots = conn.execute("""
    SELECT s.id, s.vehicle_type_id,
    CASE 
        WHEN s.id IN (SELECT slot_id FROM bookings WHERE status='booked')
        THEN 'Occupied'
        ELSE 'Available'
    END as status
    FROM slots s
    """).fetchall()

    conn.close()

    return render_template('slots.html', slots=slots)        

# ---------------- RUN APP ----------------
if __name__ == '__main__':
    app.run(debug=True, port=5001)