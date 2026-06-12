import sqlite3

def init_db():
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()

    # Admin table
    c.execute('''
        CREATE TABLE IF NOT EXISTS admin (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    
    # Insert default admin if not exists
    c.execute("SELECT * FROM admin WHERE username='pavan'")
    if not c.fetchone():
        c.execute("INSERT INTO admin (username, password) VALUES ('pavan', 'kumar1109')")

    # Staff table
    c.execute('''
        CREATE TABLE IF NOT EXISTS staff (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            classAssigned TEXT NOT NULL,
            passcode TEXT NOT NULL,
            isFirstLogin INTEGER DEFAULT 1
        )
    ''')

    # Tasks table
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            staffId TEXT NOT NULL,
            description TEXT NOT NULL,
            assignedDate TEXT NOT NULL,
            deadline TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            FOREIGN KEY (staffId) REFERENCES staff (id)
        )
    ''')

    # Students table
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            class TEXT NOT NULL,
            section TEXT NOT NULL,
            passcode TEXT NOT NULL,
            isFirstLogin INTEGER DEFAULT 1
        )
    ''')

    # Exams table
    c.execute('''
        CREATE TABLE IF NOT EXISTS exams (
            id TEXT PRIMARY KEY,
            studentId TEXT NOT NULL,
            examName TEXT NOT NULL,
            subject TEXT NOT NULL,
            marksObtained INTEGER NOT NULL,
            totalMarks INTEGER NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (studentId) REFERENCES students (id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == '__main__':
    init_db()
