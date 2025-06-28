import sqlite3

conn = sqlite3.connect('instance/studentPortal.db')
cursor = conn.cursor()

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables in database:")
for table in cursor.fetchall():
    print(table[0])

conn.close()