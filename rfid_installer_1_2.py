import time

import subprocess
import sys


required_modules = [
    "pathlib",
    "time","tkinter","random",
    "datetime",
    "pymysql",
    "tkcalendar",
    "reportlab",
    "datetime",
    "pyserial",
    "db-sqlite3"
]

sucful=[]
unsucful=[]
def install_modules(modules):

    for module in modules:
        try:
            print(f"Installing {module}...")
            subprocess.check_call(["pip", "install", module])
            print(f"Successfully installed {module}.")
            sucful.append(module)
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {module}: {e}")
            unsucful.append(module)
    print("\n")

    if len(sucful) == len(required_modules):
        print("-------------------------\nInstallation Report :\n")
        print('''SuccessfulL installed all the modules : DONE\n-------------------------''')
    else:
        print("-------------------------\nInstallation Report :\n")
        print("UnSuccessfully!!!  = ", unsucful)
        print("Successfull  = ", sucful)
        print("-------------------------\n")

def check_imports(required_modules):
    missing_modules=[]

    print("Importing Report :\n")
    for module_name in required_modules:
        try:
            __import__(module_name)
            print(f" Module '{module_name}' installed and importable : DONE")
        except ImportError:
            missing_modules.append(module_name)
            print(f" ---> Import error for '{module_name}' : ERROR")
    print("-------------------------")



install_modules(required_modules)
#print("checking for Imports\n")
check_imports(required_modules)



for i in range(7, 0, -1):
    # Print the remaining time
    print(f"Starting Database Setup in: {i} seconds")

    # Sleep for a second to simulate time passing
    time.sleep(1)

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
