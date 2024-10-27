import sqlite3

# Initialize the SQLite database
def create_db():
    conn = sqlite3.connect('railway.db')
    
    # Drop existing tables if they exist
    conn.execute('DROP TABLE IF EXISTS users')
    conn.execute('DROP TABLE IF EXISTS train_info')
    conn.execute('DROP TABLE IF EXISTS ticket_booking')
    
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
            arrival_time TEXT NOT NULL,
            price REAL NOT NULL
        )
    ''')
    
    # Create ticket_booking table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS ticket_booking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            train_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            window_seat_preference BOOLEAN NOT NULL,
            train_no TEXT NOT NULL,
            train_name TEXT NOT NULL,
            coach TEXT NOT NULL,
            coach_number TEXT NOT NULL,
            seat_no INTEGER NOT NULL,
            travel_date TEXT NOT NULL,
            time_of_booking TEXT NOT NULL,
            no_of_adults INTEGER NOT NULL,
            no_of_children INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (train_id) REFERENCES train_info(id)
        )
    ''')
    
    # Insert initial train data
    conn.execute('''
        INSERT INTO train_info (train_no, train_name, source, destination, departure_time, arrival_time, price) 
VALUES 
    -- Mumbai to Delhi
    ('101', 'Mumbai Express', 'Mumbai', 'Delhi', '06:00', '18:00', 1800.0),
    ('102', 'Mumbai Rajdhani', 'Mumbai', 'Delhi', '16:00', '08:00', 2500.0),
    ('103', 'Mumbai Duronto', 'Mumbai', 'Delhi', '22:00', '09:30', 1900.0),
    
    -- Delhi to Mumbai
    ('104', 'Delhi Express', 'Delhi', 'Mumbai', '07:00', '19:00', 1800.0),
    ('105', 'Delhi Rajdhani', 'Delhi', 'Mumbai', '20:30', '10:00', 2500.0),
    ('106', 'Delhi Duronto', 'Delhi', 'Mumbai', '23:00', '12:00', 1900.0),

    -- Mumbai to Chennai
    ('107', 'Mumbai-Chennai Mail', 'Mumbai', 'Chennai', '05:00', '19:00', 2000.0),
    ('108', 'Mumbai-Chennai Superfast', 'Mumbai', 'Chennai', '15:30', '06:30', 2200.0),
    
    -- Chennai to Mumbai
    ('109', 'Chennai-Mumbai Express', 'Chennai', 'Mumbai', '06:30', '21:00', 2000.0),
    ('110', 'Chennai-Mumbai Duronto', 'Chennai', 'Mumbai', '17:00', '07:30', 2200.0),

    -- Mumbai to Kolkata
    ('111', 'Mumbai-Kolkata Express', 'Mumbai', 'Kolkata', '06:00', '23:30', 2300.0),
    ('112', 'Mumbai-Kolkata Superfast', 'Mumbai', 'Kolkata', '18:30', '12:30', 2500.0),

    -- Kolkata to Mumbai
    ('113', 'Kolkata-Mumbai Express', 'Kolkata', 'Mumbai', '05:30', '23:00', 2300.0),
    ('114', 'Kolkata-Mumbai Humsafar', 'Kolkata', 'Mumbai', '17:00', '10:00', 2500.0),

    -- Mumbai to Bangalore
    ('115', 'Mumbai-Bangalore Express', 'Mumbai', 'Bangalore', '06:00', '20:00', 2000.0),
    ('116', 'Mumbai-Bangalore Duronto', 'Mumbai', 'Bangalore', '18:00', '09:30', 2300.0),
    
    -- Bangalore to Mumbai
    ('117', 'Bangalore-Mumbai Express', 'Bangalore', 'Mumbai', '05:30', '19:30', 2000.0),
    ('118', 'Bangalore-Mumbai Superfast', 'Bangalore', 'Mumbai', '17:30', '09:00', 2300.0),

    -- Delhi to Chennai
    ('119', 'Delhi-Chennai Express', 'Delhi', 'Chennai', '06:00', '22:30', 2200.0),
    ('120', 'Delhi-Chennai Rajdhani', 'Delhi', 'Chennai', '16:00', '09:30', 2500.0),

    -- Chennai to Delhi
    ('121', 'Chennai-Delhi Express', 'Chennai', 'Delhi', '07:30', '23:00', 2200.0),
    ('122', 'Chennai-Delhi Rajdhani', 'Chennai', 'Delhi', '18:00', '10:30', 2500.0),

    -- Delhi to Kolkata
    ('123', 'Delhi-Kolkata Mail', 'Delhi', 'Kolkata', '08:00', '23:00', 2000.0),
    ('124', 'Delhi-Kolkata Duronto', 'Delhi', 'Kolkata', '18:00', '10:30', 2300.0),

    -- Kolkata to Delhi
    ('125', 'Kolkata-Delhi Express', 'Kolkata', 'Delhi', '06:00', '22:30', 2000.0),
    ('126', 'Kolkata-Delhi Rajdhani', 'Kolkata', 'Delhi', '19:00', '09:00', 2300.0),

    -- Delhi to Bangalore
    ('127', 'Delhi-Bangalore Express', 'Delhi', 'Bangalore', '05:30', '21:30', 2100.0),
    ('128', 'Delhi-Bangalore Humsafar', 'Delhi', 'Bangalore', '15:00', '08:00', 2400.0),

    -- Bangalore to Delhi
    ('129', 'Bangalore-Delhi Express', 'Bangalore', 'Delhi', '06:00', '22:30', 2100.0),
    ('130', 'Bangalore-Delhi Rajdhani', 'Bangalore', 'Delhi', '17:30', '09:30', 2400.0),

    -- Chennai to Kolkata
    ('131', 'Chennai-Kolkata Mail', 'Chennai', 'Kolkata', '08:00', '23:30', 2100.0),
    ('132', 'Chennai-Kolkata Superfast', 'Chennai', 'Kolkata', '20:00', '12:30', 2400.0),

    -- Kolkata to Chennai
    ('133', 'Kolkata-Chennai Express', 'Kolkata', 'Chennai', '06:30', '22:00', 2100.0),
    ('134', 'Kolkata-Chennai Duronto', 'Kolkata', 'Chennai', '18:00', '10:30', 2400.0),

    -- Chennai to Bangalore
    ('135', 'Chennai-Bangalore Shatabdi', 'Chennai', 'Bangalore', '06:00', '12:00', 900.0),
    ('136', 'Chennai-Bangalore Mail', 'Chennai', 'Bangalore', '18:30', '00:30', 900.0),

    -- Bangalore to Chennai
    ('137', 'Bangalore-Chennai Shatabdi', 'Bangalore', 'Chennai', '07:00', '13:00', 900.0),
    ('138', 'Bangalore-Chennai Superfast', 'Bangalore', 'Chennai', '18:00', '23:30', 900.0);


    ''')
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_db()
    print("Database and tables created with initial data.")