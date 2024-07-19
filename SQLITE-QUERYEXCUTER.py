import sqlite3


# Connect to the database
conn = sqlite3.connect('attendance_system.db.db')

# Create a cursor object
cur = conn.cursor()

query = '''SELECT name FROM sqlite_master WHERE type='table';





        '''



try:

    cur.execute(query)
    result=cur.fetchone()
    print(f"{result}\n{query}")
    print("QUERY OK")
    conn.commit()

except Exception as e:
    print(f"\n{e}")



conn.close()