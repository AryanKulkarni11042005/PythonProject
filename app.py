from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search_trains', methods=['GET', 'POST'])
def search_trains():
    if request.method == 'POST':
        from_location = request.form['from_location']
        to_location = request.form['to_location']
        travel_date = request.form['travel_date']
        
        conn = sqlite3.connect('railway.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, train_no, train_name, source, destination, departure_time, arrival_time, price
            FROM train_info
            WHERE source = ? AND destination = ?
        ''', (from_location, to_location))
        
        trains = cursor.fetchall()
        conn.close()
        
        return render_template('select_train.html', trains=trains, travel_date=travel_date)
    
    return render_template('search_trains.html')

@app.route('/book_ticket', methods=['GET', 'POST'])
def book_ticket():
    if request.method == 'GET':
        train_id = request.args.get('train_id')
        travel_date = request.args.get('travel_date')
        return render_template('book_ticket.html', train_id=train_id, travel_date=travel_date)
    
    if request.method == 'POST':
        print(request.form)  # Debugging statement to check form data
        required_fields = ['train_id', 'travel_date', 'name', 'age', 'phone', 'email', 'coach']
        missing_fields = [field for field in required_fields if field not in request.form]
        
        if missing_fields:
            print(f"Missing form fields: {', '.join(missing_fields)}")
            flash(f"Missing form fields: {', '.join(missing_fields)}", 'error')
            return redirect(url_for('search_trains'))
        
        train_id = request.form['train_id']
        travel_date = request.form['travel_date']
        name = request.form['name']
        age = request.form['age']
        phone = request.form['phone']
        email = request.form['email']
        window_seat_preference = 'window_seat_preference' in request.form
        coach = request.form['coach']
        
        # Auto-generate seat number
        seat_no = random.choice([i for i in range(1, 71) if (window_seat_preference and i % 3 == 0) or not window_seat_preference])
        
        # Generate coach number
        if coach == 'General':
            coach_number = f'G{random.randint(1, 2)}'
        else:
            coach_number = f'S{random.randint(1, 14)}'
        
        conn = sqlite3.connect('railway.db')
        cursor = conn.cursor()
        
        # Insert user data
        cursor.execute('''
            INSERT INTO users (name, age, phone, email, window_seat_preference)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, age, phone, email, window_seat_preference))
        
        user_id = cursor.lastrowid
        print(f"Inserted user with ID: {user_id}")
        
        # Fetch train information
        cursor.execute('SELECT train_no, train_name FROM train_info WHERE id = ?', (train_id,))
        train_info = cursor.fetchone()
        if not train_info:
            print(f"No train found with ID: {train_id}")
            flash(f"No train found with ID: {train_id}", 'error')
            return redirect(url_for('search_trains'))
        
        train_no, train_name = train_info
        
        # Insert ticket booking data
        cursor.execute('''
            INSERT INTO ticket_booking (user_id, train_id, name, age, phone, email, window_seat_preference, train_no, train_name, coach, coach_number, seat_no, travel_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, train_id, name, age, phone, email, window_seat_preference, train_no, train_name, coach, coach_number, seat_no, travel_date))
        
        ticket_id = cursor.lastrowid
        conn.commit()
        print(f"Inserted ticket with user_id: {user_id}, train_id: {train_id}, seat_no: {seat_no}, travel_date: {travel_date}")
        
        # Fetch the ticket information
        cursor.execute('SELECT * FROM ticket_booking WHERE id = ?', (ticket_id,))
        ticket_info = cursor.fetchone()
        
        conn.close()
        
        return render_template('booking_success.html', ticket=ticket_info)

@app.route('/view_tickets')
def view_tickets():
    conn = sqlite3.connect('railway.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM ticket_booking')
    
    tickets = cursor.fetchall()
    print(f"Retrieved tickets: {tickets}")  # Debugging statement to check fetched tickets
    conn.close()
    
    return render_template('view_tickets.html', tickets=tickets)

@app.route('/ticket_view/<int:ticket_id>')
def ticket_view(ticket_id):
    conn = sqlite3.connect('railway.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM ticket_booking WHERE id = ?', (ticket_id,))
    ticket = cursor.fetchone()
    conn.close()
    
    if not ticket:
        flash('Ticket not found', 'error')
        return redirect(url_for('view_tickets'))
    
    return render_template('ticket_view.html', ticket=ticket)

@app.route('/cancel_ticket', methods=['GET', 'POST'])
def cancel_ticket():
    if request.method == 'POST':
        ticket_id = request.form['ticket_id']
        
        conn = sqlite3.connect('railway.db')
        cursor = conn.cursor()
        
        # Delete the ticket booking
        cursor.execute('DELETE FROM ticket_booking WHERE id = ?', (ticket_id,))
        
        conn.commit()
        conn.close()
        
        flash('Ticket canceled successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('cancel_ticket.html')

if __name__ == '__main__':
    app.run(debug=True)