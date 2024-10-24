from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# SQLite database setup
DATABASE = 'railway.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Routes for the application
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book-ticket', methods=['GET', 'POST'])
def book_ticket():
    if request.method == 'POST':
        name = request.form['name']
        train_no = request.form['train_no']
        seat_no = request.form['seat_no']

        if not name or not train_no or not seat_no:
            flash("All fields are required!", "error")
            return redirect(url_for('book_ticket'))

        conn = get_db_connection()
        conn.execute("INSERT INTO tickets (name, train_no, seat_no) VALUES (?, ?, ?)", (name, train_no, seat_no))
        conn.commit()
        conn.close()

        flash('Ticket booked successfully!', 'success')
        return redirect(url_for('view_tickets'))
    return render_template('book_ticket.html')

@app.route('/view-tickets')
def view_tickets():
    conn = get_db_connection()
    tickets = conn.execute("SELECT * FROM tickets").fetchall()
    conn.close()
    return render_template('view_tickets.html', tickets=tickets)

@app.route('/cancel-ticket', methods=['GET', 'POST'])
def cancel_ticket():
    if request.method == 'POST':
        ticket_id = request.form['ticket_id']
        conn = get_db_connection()
        conn.execute("DELETE FROM tickets WHERE id = ?", (ticket_id,))
        conn.commit()
        conn.close()

        flash('Ticket cancelled successfully!', 'success')
        return redirect(url_for('view_tickets'))
    return render_template('cancel_ticket.html')

if __name__ == '__main__':
    app.run(debug=True)
