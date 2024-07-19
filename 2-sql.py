import sqlite3

# Set up a connection to the database
connection = sqlite3.connect('attendance_system.db')

try:
    # Create a new cursor
    cursor = connection.cursor()

    # Execute the SQL queries
    cursor.execute('''
        CREATE TABLE registered_users (
          
          name VARCHAR(255) NOT NULL,
          roll_no VARCHAR(255) NOT NULL UNIQUE,
          rfid_number VARCHAR(255) NOT NULL PRIMARY KEY,
          category VARCHAR(255) NOT NULL
        );
    ''')

    cursor.execute('''
        CREATE TABLE cred(
          
          username VARCHAR(255) NOT NULL PRIMARY KEY,
          password VARCHAR(255) NOT NULL
        );
    ''')

    cursor.execute('''
        CREATE TABLE att_2024_04_20 (
    rfid VARCHAR(255) NOT NULL,
    timestamp DATETIME DEFAULT (datetime('now', 'localtime')),
    roll_no VARCHAR(255) NOT NULL
    );

    ''')

    cursor.execute('''CREATE TABLE quick_att (
          
          rfid VARCHAR(255) NOT NULL ,
          timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
          roll_no VARCHAR(255)  NOT NULL);
          ''')

    cursor.execute("insert into cred (username,password) values ('admin','123'),('adhi','1732109357')")
    # Commit the changes
    connection.commit()

    print('Tables created successfully\n SQL IS ALL SET')

except Exception as e:
    print(f"\n{e}")

finally:
    # Close the connection
    connection.close()