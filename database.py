import sqlite3

# Initialize the SQLite database
def create_db():
    conn = sqlite3.connect('railway.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            train_no TEXT NOT NULL,
            seat_no TEXT NOT NULL
        )
    ''')
    conn.close()

if __name__ == '__main__':
    create_db()
    print("Database and tables created.")
