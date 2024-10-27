from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import random
from datetime import datetime, timedelta

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
        required_fields = ['train_id', 'travel_date', 'name', 'age', 'phone', 'email', 'coach', 'no_of_adults', 'no_of_children']
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
        no_of_adults = int(request.form['no_of_adults'])
        no_of_children = int(request.form['no_of_children'])
        
        # Auto-generate seat number
        seat_no = random.choice([i for i in range(1, 71) if (window_seat_preference and i % 3 == 0) or not window_seat_preference])
        
        # Generate coach number
        if coach == 'General':
            coach_number = f'G{random.randint(1, 2)}'
        else:
            coach_number = f'S{random.randint(1, 14)}'
        
        # Get current time as time of booking
        time_of_booking = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
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
        cursor.execute('SELECT train_no, train_name, price FROM train_info WHERE id = ?', (train_id,))
        train_info = cursor.fetchone()
        if not train_info:
            print(f"No train found with ID: {train_id}")
            flash(f"No train found with ID: {train_id}", 'error')
            return redirect(url_for('search_trains'))
        
        train_no, train_name, price_per_ticket = train_info
        
        # Calculate total amount
        total_amount = (no_of_adults + no_of_children * 0.5) * price_per_ticket
        
        # Insert ticket booking data
        cursor.execute('''
            INSERT INTO ticket_booking (user_id, train_id, name, age, phone, email, window_seat_preference, train_no, train_name, coach, coach_number, seat_no, travel_date, time_of_booking, no_of_adults, no_of_children)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, train_id, name, age, phone, email, window_seat_preference, train_no, train_name, coach, coach_number, seat_no, travel_date, time_of_booking, no_of_adults, no_of_children))
        
        ticket_id = cursor.lastrowid
        conn.commit()
        print(f"Inserted ticket with user_id: {user_id}, train_id: {train_id}, seat_no: {seat_no}, travel_date: {travel_date}")
        
        # Fetch the ticket information
        cursor.execute('SELECT * FROM ticket_booking WHERE id = ?', (ticket_id,))
        ticket_info = cursor.fetchone()
        
        conn.close()
        
        return render_template('payment.html', ticket=ticket_info, total_amount=total_amount, price_per_ticket=price_per_ticket)

@app.route('/confirm_booking/<int:ticket_id>', methods=['POST'])
def confirm_booking(ticket_id):
    conn = sqlite3.connect('railway.db')
    cursor = conn.cursor()
    
    # Fetch the ticket information
    cursor.execute('''
        SELECT tb.*, ti.price
        FROM ticket_booking tb
        JOIN train_info ti ON tb.train_id = ti.id
        WHERE tb.id = ?
    ''', (ticket_id,))
    
    ticket = cursor.fetchone()
    
    conn.close()
    
    if not ticket:
        flash('Ticket not found', 'error')
        return redirect(url_for('view_tickets'))
    
    no_of_adults = ticket[15]
    no_of_children = ticket[16]
    price_per_ticket = ticket[-1]
    total_amount = (no_of_adults + no_of_children * 0.5) * price_per_ticket
    
    flash('Ticket booked successfully!', 'success')
    return render_template('booking_success.html', ticket=ticket, total_amount=total_amount)

@app.route('/view_tickets')
def view_tickets():
    conn = sqlite3.connect('railway.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT tb.*, ti.price
        FROM ticket_booking tb
        JOIN train_info ti ON tb.train_id = ti.id
    ''')
    
    tickets = cursor.fetchall()
    conn.close()
    
    tickets_with_amount = []
    for ticket in tickets:
        no_of_adults = ticket[15]
        no_of_children = ticket[16]
        price_per_ticket = ticket[-1]
        total_amount = (no_of_adults + no_of_children * 0.5) * price_per_ticket
        tickets_with_amount.append((ticket, total_amount))
    
    return render_template('view_tickets.html', tickets=tickets_with_amount)

@app.route('/ticket_view/<int:ticket_id>')
def ticket_view(ticket_id):
    conn = sqlite3.connect('railway.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT tb.*, ti.price
        FROM ticket_booking tb
        JOIN train_info ti ON tb.train_id = ti.id
        WHERE tb.id = ?
    ''', (ticket_id,))
    
    ticket = cursor.fetchone()
    
    conn.close()
    
    if not ticket:
        flash('Ticket not found', 'error')
        return redirect(url_for('view_tickets'))
    
    no_of_adults = ticket[15]
    no_of_children = ticket[16]
    price_per_ticket = ticket[-1]
    total_amount = (no_of_adults + no_of_children * 0.5) * price_per_ticket
    
    return render_template('ticket_view.html', ticket=ticket, total_amount=total_amount)

@app.route('/cancel_ticket', methods=['GET'])
def cancel_ticket():
    conn = sqlite3.connect('railway.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT tb.*, ti.price
        FROM ticket_booking tb
        JOIN train_info ti ON tb.train_id = ti.id
    ''')
    
    tickets = cursor.fetchall()
    conn.close()
    
    tickets_with_amount = []
    for ticket in tickets:
        no_of_adults = ticket[15]
        no_of_children = ticket[16]
        price_per_ticket = ticket[-1]
        total_amount = (no_of_adults + no_of_children * 0.5) * price_per_ticket
        tickets_with_amount.append((ticket, total_amount))
    
    return render_template('cancel_ticket.html', tickets=tickets_with_amount)

@app.route('/confirm_cancel_ticket')
def confirm_cancel_ticket():
    ticket_id = request.args.get('ticket_id')
    
    conn = sqlite3.connect('railway.db')
    cursor = conn.cursor()
    
    # Fetch the ticket information
    cursor.execute('SELECT time_of_booking FROM ticket_booking WHERE id = ?', (ticket_id,))
    ticket = cursor.fetchone()
    
    if not ticket:
        return jsonify({'status': 'error', 'message': 'Ticket not found'})
    
    time_of_booking = datetime.strptime(ticket[0], '%Y-%m-%d %H:%M:%S')
    current_time = datetime.now()
    
    # Check if the booking time is less than 24 hours
    if current_time - time_of_booking < timedelta(hours=24):
        refund_message = 'Refund will be disbursed.'
    else:
        refund_message = 'No refund will be disbursed.'
    
    # Delete the ticket booking
    cursor.execute('DELETE FROM ticket_booking WHERE id = ?', (ticket_id,))
    
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success', 'message': 'Ticket canceled successfully!', 'refund_message': refund_message})

if __name__ == '__main__':
    app.run(debug=True)