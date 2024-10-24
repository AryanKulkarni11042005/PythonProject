from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book_ticket', methods=['GET', 'POST'])
def book_ticket():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        phone = request.form['phone']
        email = request.form['email']
        window_seat_preference = 'window_seat_preference' in request.form
        train_no = request.form['train_no']
        seat_no = request.form['seat_no']
        
        conn = sqlite3.connect('railway.db')
        cursor = conn.cursor()
        
        # Insert user data
        cursor.execute('''
            INSERT INTO users (name, age, phone, email, window_seat_preference)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, age, phone, email, window_seat_preference))
        
        user_id = cursor.lastrowid
        print(f"Inserted user with ID: {user_id}")
        
        # Get train_id from train_no
        cursor.execute('SELECT id FROM train_info WHERE train_no = ?', (train_no,))
        train = cursor.fetchone()
        
        if train is None:
            conn.close()
            flash('Train number does not exist.', 'error')
            return redirect(url_for('book_ticket'))
        
        train_id = train[0]
        print(f"Found train with ID: {train_id}")
        
        # Insert ticket booking data
        cursor.execute('''
            INSERT INTO ticket_booking (user_id, train_id, seat_no)
            VALUES (?, ?, ?)
        ''', (user_id, train_id, seat_no))
        
        conn.commit()
        conn.close()
        
        flash('Ticket booked successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('book_ticket.html')

@app.route('/view_tickets')
def view_tickets():
    conn = sqlite3.connect('railway.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT users.name, users.age, users.phone, users.email, users.window_seat_preference,
               train_info.train_no, train_info.train_name, ticket_booking.seat_no
        FROM ticket_booking
        JOIN users ON ticket_booking.user_id = users.id
        JOIN train_info ON ticket_booking.train_id = train_info.id
    ''')
    
    tickets = cursor.fetchall()
    print(f"Retrieved tickets: {tickets}")
    conn.close()
    
    return render_template('view_tickets.html', tickets=tickets)

@app.route('/cancel_ticket')
def cancel_ticket():
    # Implement the logic for canceling a ticket
    return render_template('cancel_ticket.html')

if __name__ == '__main__':
    app.run(debug=True)