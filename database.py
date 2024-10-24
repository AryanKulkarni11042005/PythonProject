import sqlite3

# Initialize the SQLite database
def create_db():
    conn = sqlite3.connect('railway.db')
    
    # Create users table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            window_seat_preference BOOLEAN NOT NULL
        )
    ''')
    
    # Create train_info table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS train_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            train_no TEXT NOT NULL,
            train_name TEXT NOT NULL,
            source TEXT NOT NULL,
            destination TEXT NOT NULL,
            departure_time TEXT NOT NULL,
            arrival_time TEXT NOT NULL
        )
    ''')
    
    # Create ticket_booking table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS ticket_booking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            train_id INTEGER NOT NULL,
            seat_no TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (train_id) REFERENCES train_info(id)
        )
    ''')
    
    # Insert initial train data
    conn.execute('''
        INSERT INTO train_info (train_no, train_name, source, destination, departure_time, arrival_time)
        VALUES ('100', 'Express Train', 'City A', 'City B', '08:00', '12:00')
    ''')
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_db()
    print("Database and tables created with initial data.")