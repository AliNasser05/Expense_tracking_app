import sqlite3

DB_NAME = "expenses.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Categories
    c.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    ''')

    # Expenses
    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER,
            description TEXT,
            amount REAL,
            FOREIGN KEY(category_id) REFERENCES categories(id)
        )
    ''')

    conn.commit()
    conn.close()

def add_category(name):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def add_expense(category, description, amount):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # ensure category exists
    c.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (category,))
    # insert expense
    c.execute("SELECT id FROM categories WHERE name=?", (category,))
    category_id = c.fetchone()[0]
    c.execute("INSERT INTO expenses (category_id, description, amount) VALUES (?, ?, ?)",
              (category_id, description, amount))
    conn.commit()
    conn.close()

def get_summary():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        SELECT categories.name, SUM(expenses.amount)
        FROM expenses
        JOIN categories ON expenses.category_id = categories.id
        GROUP BY categories.name
    ''')
    result = dict(c.fetchall())
    conn.close()
    return result

def get_all_expenses():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        SELECT categories.name, expenses.description, expenses.amount
        FROM expenses
        JOIN categories ON expenses.category_id = categories.id
        ORDER BY expenses.id DESC
    ''')
    rows = c.fetchall()
    conn.close()
    return rows
