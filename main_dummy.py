from pathlib import Path
import os
import time
from datetime import date
import pymysql
from tkinter import *
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage,ttk
import random
from tkinter import ttk
from tkcalendar import DateEntry
import datetime
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import threading
import paho.mqtt.client as mqtt
from babel import numbers

#mqtt--------
broker_address = "0.tcp.ap.ngrok.io"
topic_name = "rfid"
username = "adhi"
password = "adhi4444"


# MySQL Connection Configuration
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'adhi4444'
DB_NAME = 'attendance_system'

connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
cursor = connection.cursor()

"""# Create a table for registered users if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS registered_users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    roll_no VARCHAR(255) NOT NULL,
                    rfid_number VARCHAR(255) NOT NULL
                )''')"""

window = Tk()
window.title('main Dummy')
window.geometry("1250x1032")
window.attributes('-fullscreen', True)

def rerun_program():
    #window.destroy()  # Close the current window
    main()
def login():
    # button_1.place_forget()
    # global button_1,button_2,button_3,button_4,button_5,button_6,button_7,button_8,l1
    global window

    status1.place_forget()
    name_label.place_forget()
    name_entry.place_forget()
    search_button.place_forget()
    roll_number_label.place_forget()
    attendance_table.place_forget()
    button_2.place_forget()
    button_3.place_forget()
    button_4.place_forget()
    button_5.place_forget()
    button_6.place_forget()
    button_7.place_forget()
    button_8.place_forget()
    l1.place_forget()
    ltime.place_forget()


    def check_user():
        try:
            # Fetch the password from the database
            selected_user = user_var.get()
            entered_password = password_entry.get()
            query = f"SELECT password FROM cred WHERE username = '{selected_user}'"
            cursor.execute(query)
            result = cursor.fetchone()

            # Check if user exists and password is correct
            if result and result[0] == entered_password:
                # messagebox.showinfo("Success", "Login successful!")
                down_label = Label(window, text="Login successful!", bg="green", fg="white",
                                   font=("Arial", 30, 'bold'))
                down_label.place(x=329.0, y=727.0, width=809.0, height=59.0)
                rerun_program()
            else:
                # messagebox.showerror("Error", "Invalid username or password")
                down_label = Label(window, text="Invalid username or password", bg="red", fg="white",
                                   font=("Arial", 30, 'bold'))
                down_label.place(x=329.0, y=727.0, width=809.0, height=59.0)
        except Exception as e:
            # messagebox.showerror("Error", f"An error occurred: {str(e)}")
            down_label = Label(window, text=f"An error occurred: {str(e)}", bg="red", fg="white",
                               font=("Arial", 30, 'bold'))
            down_label.place(x=329.0, y=727.0, width=809.0, height=59.0)



    password_label = Label(window, text="Password:",font=("Arial", 40,'bold'), fg="white",bg="#ad8140")
    password_label.place(x=485.0, y=485.0, width=226.0, height=59.0)
    password_entry = Entry(window, show="*",font=("Arial", 40,'bold'), fg="#ad8140",bg="white")
    password_entry.place(x=741.0, y=485.0, width=226.0, height=59.0)
    user_label = Label(window, text="User:", font=("Arial", 40,'bold'), fg="white",bg="#ad8140")
    user_label.place(x=485.0, y=391.0, width=226.0, height=59.0)

    # Create a dropdown for user selection
    user_var = StringVar(window)
    user_var.set("admin")  # Default selection
    user_dropdown = OptionMenu(window, user_var, "admin", "student",)
    user_dropdown.config(font=("Arial", 20,'bold'), fg="blue",bg="#ad8140")
    user_dropdown.place(x=741.0, y=391.0, width=226.0, height=59.0)

    # Create a button to login
    login_button = Button(window, text="Login", command=check_user,fg="#1d2f71", font=("Arial", 25,'bold'))
    login_button.place(x=491.0, y=599.0, width=466.0, height=47.0)


def main():
    global window,Canvas
    global button_1, button_2, button_3, button_4, button_5, button_6, button_7, button_8, l1,status,status0,status1
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"/Users/adhilogu2004gmail.com/Downloads/build/assets/frame0")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    def my_time():
        time_string = time.strftime('%I:%M:%S %p / %d-%m-%Y')
        l1.config(text=time_string)
        l1.after(1000, my_time)

    """def on_connect(client, userdata, flags, rc):
        #print("Connected with result code " + str(rc))
        client.subscribe(topic_name)

    # Define the on_message callback function
    def on_message(client, userdata, msg):
        # print(msg.payload)
        byte_string = msg.payload
        string_value = byte_string.decode('utf-8')
        print(string_value)"""



    canvas = Canvas(
        window,

        height=1350,
        width=1550,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        640.0,
        416.0,
        image=image_image_1
    )
    # logo
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: login,
        relief="flat"
    )
    button_1.place(
        x=142.0,
        y=46.0,
        width=1136.0,
        height=166.0
    )
    # time
    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: my_time,
        relief="flat"
    )
    button_2.place(
        x=412.0,
        y=244.0,
        width=595.0,
        height=86.0
    )

    def attendance_menu(): #######attendance----------------------------
        # hide the existing buttons
        global button_image_1,ltime,name_label,name_entry,search_button,roll_number_label,attendance_table,status1,status0,name
        button_1.place_forget()
        button_2.place_forget()
        button_3.place_forget()
        button_4.place_forget()
        button_5.place_forget()
        button_6.place_forget()
        button_7.place_forget()
        button_8.place_forget()
        l1.place_forget()

        """def on_message(client, userdata, msg):
            global mqtt_message
            byte_string = msg.payload
            string_value = byte_string.decode('utf-8')
            mqtt_message = string_value
            #scan_rfid = Label(window, text=mqtt_message, font=my_font, borderwidth=0,highlightthickness=0, bg="#ad8140", fg="#1d2f71")
            #scan_rfid.place(x=642, y=340, width=328, height=66)
            current_atte(mqtt_message)
            print(mqtt_message)

        client.on_message = on_message"""

        def update_attendance_table():

            cursor.execute("SELECT * FROM att_2024_04_20")
            data = cursor.fetchall()

            for row in attendance_table.get_children():
                attendance_table.delete(row)
            for record in data:

                attendance_table.insert('','end',text=record[0],values=record[1:4])

        my_font = ('times', 50, 'bold')
        ltime = Button(window, font=my_font, borderwidth=0,
                    highlightthickness=0, bg="#ad81ff", fg="#ad8140")
        ltime.place(x=740.0,
                 y=330.0,
                 width=595.0,
                 height=86.0)
        today = date.today().strftime("%Y_%m_%d")
        attendance_table = ttk.Treeview(window, columns=("RF Number", "Time Stamp","Roll Number"))
        # Create an instance of Style widget
        style = ttk.Style()
        style.theme_use('aqua')

        #attendance_table.column("# 0", anchor=CENTER, stretch=NO, width=150)
        #attendance_table.heading("RF Number", text="RF Number")
        attendance_table.heading("#0", text="S.no")
        attendance_table.column("# 0", anchor=CENTER, stretch=NO, width=60)
        attendance_table.heading("RF Number", text="RF Number")
        attendance_table.column("# 1", anchor=CENTER, stretch=NO,width=160)
        attendance_table.heading("Time Stamp", text="Time Stamp")
        attendance_table.column("# 2", anchor=CENTER, stretch=NO, width=140)
        attendance_table.heading("Roll Number", text="Roll Number")
        attendance_table.column("# 3", anchor=CENTER, stretch=NO, width=130)
        attendance_table.place(x=70,y=325,width=600.0,heigh=552.0)

        def current_atte(mqtt_message):
            global status0,status1
            name = mqtt_message
            cursor.execute("SELECT roll_no FROM registered_users WHERE rfid_number = %s", (name,))
            result = cursor.fetchone()
            if result:
                name_of = cursor.execute(f"SELECT name FROM registered_users WHERE rfid_number = %s",(name,))
                name_of = cursor.fetchone()
                name_of_roll=name_of[0].upper()
                cursor.execute(f"INSERT INTO att_2024_04_20 (rfid) VALUES (%s)",(name,))
                roll_number = result[0]  # Assuming roll_number is the first column in the query result
                roll_number_label.config(text=f"{roll_number}\n{name_of_roll}")
                status1 = Label(window, text="PRESENT", font=my_font, borderwidth=0,
                                          highlightthickness=0, bg="green", fg="white")
                status1.place(x=733.0, y=700.0, width=610.0, height=100.0)
                update_attendance_table()
                connection.commit()


            else:
                roll_number_label.config(text=f"Unknown {name}")
                status1 = Label(window, text="UNKNOWN", font=my_font, borderwidth=0,
                               highlightthickness=0, bg="red", fg="white")
                status1.place(x=733.0, y=700.0, width=610.0, height=100.0)
        ##sample----------------------
        name_label = Label(window, text="Enter Name:")
        name_entry = Entry(window)
        search_button = Button(window, text="Search", command=current_atte)
        roll_number_label = Label(window, text="Next",font=my_font, borderwidth=0,highlightthickness=0, bg="#ad8140", fg="#ffffff")

        status1 = Label(window, text="----", font=my_font, borderwidth=0,highlightthickness=0, bg="#ad8140", fg="white")
        status1.place(x=733.0, y=700.0, width=610.0, height=100.0)
        # Arrange widgets using grid layout
        name_label.grid(row=0, column=0, padx=5, pady=5)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        search_button.grid(row=0, column=2, padx=5, pady=5)
        roll_number_label.place(x=733.0,y=527.0,width=610.0,height=150.0)

        #sampleee_____________
        def my_time_2():
            time_string = time.strftime('%I:%M:%S %p / %d-%m-%Y')
            ltime.config(text=time_string)
            ltime.after(1000, my_time_2)

        button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        button_logo = Button(
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: login(),
            relief="raised"
        )
        button_logo.place(
            x=142.0,
            y=46.0,
            width=1136.0,
            height=166.0
        )

        def on_key_press(event):
            if event.keysym == "Escape":
                login()

        window.bind("<Key>", on_key_press)


        my_time_2()

        update_attendance_table()


    def register_menu(): #######--------------register----------------------------
        # hide the existing buttons
        global button_image_1,ltime
        #button_1.place_forget()
        button_2.place_forget()
        button_3.place_forget()
        button_4.place_forget()
        button_5.place_forget()
        button_6.place_forget()
        button_7.place_forget()
        button_8.place_forget()
        l1.place_forget()

        def register_user():
            #global scan_rfid
            try:
                rfid = scan_rfid.cget("text")
                name = name_entry.get()
                roll_no = roll_no_entry.get()
                category = user_var.get()
                if name_entry.get().strip() != '' and roll_no_entry.get().strip() != '' and user_var.get().strip() != '':
                    cursor.execute("INSERT INTO registered_users (rfid_number , name,roll_no,category) VALUES (%s, %s, %s, %s)",
                                   (rfid, name, roll_no,category))
                    connection.commit()
                    hello_label = Label(window, text="REGISTERED SUCCESFULLY",bg="green",fg="white", font=("Arial", 20,'bold'))
                    hello_label.place(x=240, y=800, width=986, height=65)
                    name_entry.delete(0, "end")
                    roll_no_entry.delete(0, "end")
                    scan_rfid.config(text="")
                else:
                    hello_label = Label(window, text="FILL ALL THE DETAILS", bg="red", fg="white",
                                        font=("Arial", 20))
                    hello_label.place(x=240, y=800, width=986, height=65)
            except:
                hello_label = Label(window, text="ERROR IN REGISTRATION",bg="red", font=("Arial", 20))
                hello_label.place(x=240, y=800, width=986, height=65)



        def generate_random_number():
            return random.randint(10000000, 99999999)


        def scan():
            global rfid_no_entry,scan_rfid

            scan_button_1 = Button(window, text="Scanning...", fg="green", font=("Arial", 20), command=scan)
            scan_button_1.place(x=1020, y=360, width=218, height=66)
            scan_rfid=Label(window, text=generate_random_number(), font=my_font, borderwidth=0,
                  highlightthickness=0, bg="#ad8140", fg="#1d2f71")
            scan_rfid.place(x=642, y=340, width=328, height=66)
            time.sleep(1)
            scan_button_1.destroy()
            return None


        name_label =Label(window, text="Name:", font=("Arial", 40,'bold'), fg="white",bg='#ad8140')
        name_entry = Entry(window, font=("Arial", 30,'bold'), fg="black",bg='white',insertbackground='red')
        roll_no_label = Label(window, text="Roll No:", font=("Arial", 40,'bold'), fg="white",bg='#ad8140')
        roll_no_entry = Entry(window, font=("Arial", 30,'bold'), fg="black",bg='white',insertbackground='red')
        rfid_no_label = Label(window, text="RFID No:", font=("Arial", 40,'bold'), fg="white",bg='#ad8140')
        rfid_no_entry = Label(window, font=("Arial", 30,'bold'), fg="black",state='disabled',bg='#ad8140')
        scan_button = Button(window, text="Scan", fg="#1d2f71",font=("Arial", 20,'bold'),command=scan)
        submit_button = Button(window, text="Submit", fg="#1d2f71", font=("Arial", 20,'bold'), command=register_user)
        banner_label = Label(window, text="New Registration", font=("Arial", 40,'bold'),fg="white",bg='#1d2f71')
        category_label = Label(window, text="Category / Year", font=("Arial", 35, 'bold'), fg="white", bg='#ad8140')
        user_var = StringVar(window)
        user_var.set("")  # Default selection
        user_dropdown = OptionMenu(window, user_var, "1st", "2st", "3rd", "4th","PIC","INTERN","GUEST","SHORT-TERM")
        user_dropdown.config(font=("Arial", 20, 'bold'), fg="blue", bg="#ad8140")
        user_dropdown.place(x=642, y=640, width=226.0, height=59.0)


        name_label.place(x=250, y=440, width=300, height=66)
        name_entry.place(x=642, y=440, width=596, height=66)
        roll_no_label.place(x=250, y=540, width=300, height=66)
        roll_no_entry.place(x=642, y=540, width=596, height=66)
        rfid_no_label.place(x=250, y=340, width=300, height=66)
        rfid_no_entry.place(x=642, y=340, width=328, height=66)
        scan_button.place(x=1020, y=340, width=218, height=66)
        category_label.place(x=250, y=640, width=300, height=66)
        submit_button.place(x=642, y=730, width=348, height=58)

        banner_label.place(x=240, y=230, width=986, height=70)

    def view_panel(): #######viewwwwwww----------------------------
        # hide the existing buttons
        global button_image_1,ltime,Canvas,canvas,numbers

        button_1.place_forget()
        button_2.place_forget()
        button_3.place_forget()
        button_4.place_forget()
        button_5.place_forget()
        button_6.place_forget()
        button_7.place_forget()
        button_8.place_forget()
        l1.place_forget()

        def select_from_date(event=None):
            global selected_from_date
            selected_from_date = from_date_entry_date.get_date()
            from_date_entry.config(text=f"{selected_from_date}")
            #print("from",selected_from_date)

        def select_to_date(event=None):
            global selected_to_date
            selected_to_date = to_date_entry_date.get_date()
            to_date_entry.config(text=f"{selected_to_date}")

        def today_data():
            cursor.execute("select * from att_2024_04_20" )

            rows = cursor.fetchall()

            table.delete(*table.get_children())

            # Insert fetched data into the Treeview widget
            for i, row in enumerate(rows, start=1):
                table.insert('', 'end', text=row[0], values=row[1:5])
                print(rows)

            # Close the cursor and connection


            table.heading("#0", text="S.no")
            table.heading("#1", text="RF Number")
            table.heading("#2", text="Time Stamp")
            table.heading("#3", text="Roll Number")

            headers = ["ID", "RFID-Number", "Time Stamp", "Roll Number"]

            # Define column widths
            table.column("#0", anchor="center", width=80)
            table.column("#1", anchor="center", width=180)
            table.column("#2", anchor="center", width=180)
            table.column("#3", anchor="center", width=190)

            table.place(x=75, y=190, width=615.0, heigh=637.0)

            hello_label = Label(window, text="Today's Attendance", bg="green", font=("Arial", 20))
            hello_label.place(x=813, y=150, width=600, height=75)
            connection.commit()


        def view_data():
            global canvas
            # Get values from entry widgets
            global rows,headers,query
            rfid_number = rfid_number_entry.get()
            roll_number = roll_number_entry.get()
            month = month_entry.get()


            # Check if any textbox is empty, if so, ignore
            """if not rfid_number or not roll_number or not selected_from_date or not selected_to_date:
                hello_label = Label(window, text="ENTER REQUIREMENT", bg="red", font=("Arial", 20))
                hello_label.place(x=813, y=150, width=600, height=75)
                return"""


            try:
                query = "SELECT * FROM att_2024_04_20 WHERE "
                conditions = []
                if rfid_number:
                    conditions.append(f"rfid = '{rfid_number}'")
                if roll_number:
                    roll_number_list = roll_number.split(',')
                    roll_number_conditions = []
                    for roll_number in roll_number_list:
                        roll_number_conditions.append(f"roll_no = '{roll_number.strip()}'")
                    roll_number_condition = ' OR '.join(roll_number_conditions)
                    conditions.append(f"({roll_number_condition})")
                if selected_from_date and selected_to_date:
                    conditions.append(f"timestamp BETWEEN '{selected_from_date}' AND '{selected_to_date}'")
                query += " AND ".join(conditions)
            except:
                hello_label = Label(window, text="TWO REQUIREMENTS NEEDED (ENTER DATE)", bg="red", font=("Arial", 20))
                hello_label.place(x=813, y=150, width=600, height=75)


            # Execute the query

            cursor.execute(query)
            rows = cursor.fetchall()

            table.delete(*table.get_children())

            # Insert fetched data into the Treeview widget
            for i, row in enumerate(rows, start=1):
                table.insert('', 'end', text=row[0], values=row[1:5])
                print(rows)

            # Close the cursor and connection

            table.heading("#0", text="ID")
            table.heading("#1", text="RFID-Number")
            table.heading("#2", text="Time Stamp")
            table.heading("#3", text="Roll Number")
            table.heading("#4", text="Category")

            headers = ["ID", "RFID-Number", "Time Stamp","Roll Number","Category"]


            # Define column widths
            table.column("#0", anchor="center", width=80)
            table.column("#1", anchor="center", width=180)
            table.column("#2", anchor="center", width=180)
            table.column("#3", anchor="center", width=190)

            table.place(x=75, y=190, width=615.0, heigh=637.0)

            hello_label = Label(window, text="Search Done", bg="green", font=("Arial", 20))
            hello_label.place(x=813, y=150, width=600, height=75)

        def calculate_working_hours():
            global rows,headers

            roll_number = roll_number_entry.get()
            rfid_number = rfid_number_entry.get()
            try:
                if not roll_number:
                    cursor.execute("""SELECT
                            a.roll_no,
                            r.name AS `Name`,
                            CONCAT(HOUR(TIMEDIFF(MAX(a.timestamp), MIN(a.timestamp))),
                                   ' hours ',
                                   MINUTE(TIMEDIFF(MAX(a.timestamp), MIN(a.timestamp))),
                                   ' minutes') AS `Total Working Hours`
                        FROM
                            att_2024_04_20 AS a
                        JOIN
                            registered_users AS r ON a.roll_no = r.roll_no
                        GROUP BY
                            a.roll_no, r.name;""")
                else:

                    roll_numbers_st = roll_number.split(',')
                    if len(roll_numbers_st) == 1 and roll_numbers_st[0].strip():
                        roll_numbers_str = (roll_numbers_st[0])
                        roll_numbers_str = '("{}")'.format(roll_numbers_str)

                    else:
                        roll_numbers_str = tuple(roll_numbers_st)


                    sql_query = f"""SELECT
                                a.roll_no,
                                r.name AS `Name`,
                                CONCAT(HOUR(TIMEDIFF(MAX(a.timestamp), MIN(a.timestamp))),
                                       ' hours ',
                                       MINUTE(TIMEDIFF(MAX(a.timestamp), MIN(a.timestamp))),
                                       ' minutes') AS `Total Working Hours`
                            FROM
                                att_2024_04_20 AS a
                            JOIN
                                registered_users AS r ON a.roll_no = r.roll_no
                            WHERE
                                a.roll_no IN {roll_numbers_str}
                            GROUP BY
                                a.roll_no, r.name;
                        """

                    # Execute the SQL query with roll_numbers_str as parameter

                    cursor.execute(sql_query)

                rows = cursor.fetchall()

                table.delete(*table.get_children())
                for i, row in enumerate(rows,start=1):
                    table.insert('', 'end', text=row[0], values=row[1:5])
                    print(rows)


                table.heading("#0", text="Roll Number")
                table.heading("#1", text="Name")
                table.heading("#2", text="Total Working Hours")

                headers = ["Roll Number", "Name", "Total Working Hours"]
                # Define column widths
                table.column("#0", anchor="center", width=190)
                table.column("#1", anchor="center", width=190)
                table.column("#2", anchor="center", width=180)

                table.place(x=75, y=190, width=615.0, heigh=637.0)
                hello_label = Label(window, text="Working Hours", bg="green", font=("Arial", 20))
                hello_label.place(x=813, y=150, width=600, height=75)
            except:
                hello_label = Label(window, text="Error in Hours Search (Enter Date)", bg="red", font=("Arial", 20))
                hello_label.place(x=813, y=150, width=600, height=75)


        logolabel = Label(window, text="VIEW PANEL", font=("Arial", 40, 'bold'), fg="#1d2f71", bg='#ad8140')
        logolabel.place(x=86, y=26, width=1294, height=83)

        def clear_table():
            table.delete(*table.get_children())

            hello_label = Label(window, text="Search", bg="#ad8140",fg="#1d2f71", font=("Arial", 30,'bold'))
            hello_label.place(x=813, y=150, width=600, height=75)

        def display_registered_users():
            # Execute the SQL query to fetch all data from registered_users table
            global rows,headers
            global canvas
            try:
                cursor.execute("SELECT * FROM registered_users")

                # Fetch all rows from the result set
                rows = cursor.fetchall()

                table.delete(*table.get_children())

                # Insert fetched data into the Treeview widget
                for i, row in enumerate(rows,start=1):
                    table.insert('', 'end', text=row[0], values=row[1:5])
                    #print(rows)

                table.heading("#0", text="ID")
                table.heading("#1", text="Name")
                table.heading("#2", text="Roll Number")
                table.heading("#3", text="RF Number")
                table.heading("#4", text="Category")

                headers = ["ID", "Name", "Roll Number", "RF Number","Category"]

                # Define column widths
                table.column("#0", anchor="center", width=80)
                table.column("#1", anchor="center", width=180)
                table.column("#2", anchor="center", width=180)
                table.column("#3", anchor="center", width=190)
                table.column("#4", anchor="center", width=100)

                table.place(x=75, y=190, width=615.0, heigh=637.0)
                hello_label = Label(window, text="All Students", bg="green", font=("Arial", 20))
                hello_label.place(x=813, y=150, width=600, height=75)

            except:
                hello_label = Label(window, text="ERROR IN USER TABLE", bg="red", font=("Arial", 20))
                hello_label.place(x=813, y=150, width=600, height=75)



        table = ttk.Treeview(window, columns=("Name", "Roll Number", "RF Number", "Time Stamp"))
        # Create an instance of Style widget
        style = ttk.Style()
        style.theme_use('aqua')

        scan_button = Button(window, text="Scan", fg="#1d2f71", font=("Arial", 20, 'bold'))


        rfid_number_entry = Entry(window, font=("Arial", 25, 'bold'), bg="white", fg='#ad8140')
        roll_number_entry = Entry(window, font=("Arial", 25, 'bold'), bg="white", fg='#ad8140')
        from_date_entry = Label(window, text="FROM",font=("Arial", 20, 'bold'), bg="white", fg='#1d2f71')
        to_date_entry = Label(window, text="TO",font=("Arial", 20, 'bold'), bg="white", fg='#1d2f71')
        month_entry = Entry(window, font=("Arial", 25, 'bold'), bg="white", fg='#ad8140')

        from_date_entry_date = DateEntry(window, width=12)
        from_date_entry_date.place(x=1043, y=460, width=157, height=25)


        to_date_entry_date = DateEntry(window, width=12)
        to_date_entry_date.place(x=1232, y=460, width=157, height=25)

        from_date_entry_date.bind("<<DateEntrySelected>>", select_from_date)
        to_date_entry_date.bind("<<DateEntrySelected>>", select_to_date)

        def present_usr():
            table.delete(*table.get_children())
            try:
                cursor.execute(f"SELECT DISTINCT ru.name, ru.roll_no FROM registered_users ru JOIN att_2024_04_20 a ON ru.roll_no = a.roll_no WHERE DATE(a.timestamp) BETWEEN '{selected_from_date}' AND '{selected_to_date}'")

                # Fetch all rows from the result set
                rows = cursor.fetchall()

                table.delete(*table.get_children())

                # Insert fetched data into the Treeview widget
                for i, row in enumerate(rows,start=1):
                    table.insert('', 'end', text=row[0], values=row[1:5])
                    #print(rows)


                table.heading("#0", text="Name")
                table.heading("#1", text="Roll Number")


                headers = ["Name","Roll Number"]

                # Define column widths
                table.column("#0", anchor="center", width=200)
                table.column("#1", anchor="center", width=200)


                table.place(x=75, y=190, width=615.0, heigh=637.0)
                hello_label = Label(window, text=f"Present Students {selected_from_date} - {selected_to_date}", bg="green", font=("Arial", 20))
                hello_label.place(x=813, y=150, width=600, height=75)

            except:
                hello_label = Label(window, text="ENTER FROM AND TO", bg="red", font=("Arial", 20))
                hello_label.place(x=813, y=150, width=600, height=75)


        def generate_pdf():
            global canvas
            try:
                downloads_dir = os.path.join(os.environ['HOME'], 'Downloads')
                timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

                # Construct the filename with the timestamp
                #filename = f"table_data_{timestamp}.pdf"
                filename = os.path.join(downloads_dir, f"table_data_{timestamp}.pdf")

                c = canvas.Canvas(filename)

                # Define table data
                data = rows

                column_widths = [20, 80, 80, 60]  # Example widths, adjust as needed

                # Set initial y coordinate for drawing the table
                y = 750

                # Draw table headers
                center_x = letter[0] / 2

                # Draw table headers
                styles = getSampleStyleSheet()
                bold_style = styles['Title']
                bold_style.fontSize = 14  # Adjust font size if needed

                for header in headers:
                    width = c.stringWidth(header, bold_style.fontName, bold_style.fontSize)
                    x = center_x - (width / 2)
                    c.setFont(bold_style.fontName, bold_style.fontSize)
                    c.drawString(x, y, header)
                    y -= 20

                # Draw table data
                for row in data:
                    y -= 20
                    x = 50
                    for item in row:
                        c.drawString(x, y, str(item))
                        x += 150

                # Save the PDF file
                c.save()
                hello_label = Label(window, text=f"PDF CREATED SUCCESSFULLY \n table_data_{timestamp}.pdf", bg="green", font=("Arial", 20))
                hello_label.place(x=813, y=150, width=600, height=75)

            except Exception as e:
                print("An error occurred:", e)
                hello_label = Label(window, text=f"PDF CREATED UNSUCCESSFULL", bg="red",font=("Arial", 20))
                hello_label.place(x=813, y=150, width=600, height=75)


        # Create buttons with individual styles
        view_button = Button(window, text="View", font=("Arial", 40, 'bold'), fg="#1d2f71",bg='#ad8140',command=view_data)
        time_spent_button = Button(window, text="Time Spent", font=("Arial", 25, 'bold'),fg="#1d2f71", bg='#ad8140',command=calculate_working_hours)
        today_button = Button(window, text="Today",  font=("Arial", 25, 'bold'), fg="#1d2f71",bg='#1d2f71',command=today_data)
        #check_button = Button(window, text="Check",  font=("Arial", 25, 'bold'), fg="#1d2f71",bg='#1d2f71')
        students_button = Button(window, text="Students",  font=("Arial", 25, 'bold'),fg="#1d2f71", bg='#ad8140',command=display_registered_users)
        print_button = Button(window, text="Print", font=("Arial", 25, 'bold'), fg="#1d2f71",bg='#ad8140',command=generate_pdf)
        clear_button = Button(window, text="Clear",  font=("Arial", 25, 'bold'), fg="#1d2f71",bg='#ad8140',command=clear_table)
        ab_button = Button(window, text="Ab", font=("Arial", 25, 'bold'), fg="#1d2f71", bg='#1d2f71')
        pr_button = Button(window, text="Pr", font=("Arial", 25, 'bold'), fg="#1d2f71", bg='#1d2f71',command=present_usr)

        # Create labels
        rfid_number_label = Label(window, text="RFID Number", font=("Arial", 30, 'bold'), fg="white", bg='#ad8140')
        roll_number_label =Label(window, text="Roll Number(s)", font=("Arial", 28, 'bold'), fg="white", bg='#ad8140')
        date_label =Label(window, text="Date", font=("Arial", 30, 'bold'), fg="white", bg='#ad8140')
        month_label = Label(window, text="Month", font=("Arial", 30, 'bold'), fg="white", bg='#ad8140')

        # Place labels
        rfid_number_label.place(x=813, y=268,width=197, height=47)
        roll_number_label.place(x=813, y=369,width=205, height=47)
        date_label.place(x=813, y=470,width=197, height=47)
        month_label.place(x=813, y=571,width=197, height=47)

        # Place buttons
        view_button.place(x=823, y=658, width=566, height=47)
        time_spent_button.place(x=823, y=738, width=157, height=47)
        today_button.place(x=823, y=804, width=157, height=47)
        ab_button.place(x=1039, y=733, width=75, height=47)
        pr_button.place(x=1119, y=733, width=75, height=47)
        students_button.place(x=1039, y=797, width=157, height=47)
        print_button.place(x=1232, y=733, width=157, height=47)
        clear_button.place(x=1232, y=797, width=157, height=47)

        # Place entry widgets
        rfid_number_entry.place(x=1023, y=263, width=223, height=59)
        roll_number_entry.place(x=1023, y=364, width=386, height=59)
        from_date_entry.place(x=1043, y=490, width=157, height=30)
        to_date_entry.place(x=1232, y=490, width=157, height=30)
        month_entry.place(x=1023, y=566, width=386, height=59)
        scan_button.place(x=1252, y=263, width=157, height=59)
        today_data()
        clear_table()

    def update_panel():
        global button_image_1, ltime, Canvas, canvas , next_btn
        button_1.place_forget()
        button_2.place_forget()
        button_3.place_forget()
        button_4.place_forget()
        button_5.place_forget()
        button_6.place_forget()
        button_7.place_forget()
        button_8.place_forget()
        l1.place_forget()

        def update_name():

            ent_label = Label(window, text="Entry New Name", font=("Arial", 25, 'bold'), fg="white", bg='green')
            ent_label.place(x=490, y=610, width=500, height=60)

            def upd_name():
                # Check if any textbox is empty, if so, ignore
                global query
                rfid_number_up = rfid_numb_ent.get()
                roll_number_up = roll_numb_ent.get()
                name_ent = detail_ent.get()
                if rfid_number_up and roll_number_up:
                    ent_label = Label(window, text="Enter Any One RF No./Roll No.", font=("Arial", 25, 'bold'), fg="white", bg='red')
                    ent_label.place(x=490, y=610, width=500, height=60)
                    return

                try:
                    query = f"UPDATE registered_users SET name ='{name_ent}' WHERE "
                    conditions = []
                    if rfid_number_up and name_ent:
                        conditions.append(f"rfid_number = '{rfid_number_up}'")
                        ent_label = Label(window, text=f"Updated {rfid_number_up}'s Name {name_ent}", font=("Arial", 25, 'bold'), fg="white",bg='green')
                        ent_label.place(x=490, y=610, width=500, height=60)
                        query += "".join(conditions)
                    elif roll_number_up and name_ent:
                        conditions.append(f"roll_no = '{roll_number_up}'")
                        ent_label = Label(window, text=f"Updated {roll_number_up}'s Name {name_ent}",
                                          font=("Arial", 25, 'bold'), fg="white", bg='green')
                        ent_label.place(x=490, y=610, width=500, height=60)
                        query += "".join(conditions)

                    else:
                        ent_label = Label(window, text="Enter RF No./Roll No. & New Name",font=("Arial", 25, 'bold'), fg="white", bg='red')
                        ent_label.place(x=490, y=610, width=500, height=60)


                except:
                    ent_label = Label(window, text=f"Error in Updating",font=("Arial", 25, 'bold'), fg="white", bg='red')
                    ent_label.place(x=490, y=610, width=500, height=60)
                cursor.execute(query)
                connection.commit()

            next_btn = Button(window, text="UPDATE", command=upd_name,font=("Arial", 25, 'bold'))
            next_btn.place(x=486, y=764, width=520, height=47)

        def delete_user():
            ent_label = Label(window, text="Enter the Roll Number(s) to Delete", font=("Arial", 25, 'bold'), fg="white", bg='green')
            ent_label.place(x=490, y=610, width=500, height=60)
            def del_user():
                global query1,query2
                rfid_number_del = rfid_numb_ent.get()
                roll_number_del = roll_numb_ent.get()
                confirm_ent = detail_ent.get()

                if not roll_number_del:
                    confirm_ent = Label(window, text="Entry Roll Number(s)", font=("Arial", 25, 'bold'), fg="white",bg='red')
                    confirm_ent.place(x=490, y=610, width=500, height=60)
                    return
                try:
                    if roll_number_del and confirm_ent=="confirm":

                        roll_number_list = roll_number_del.split(',')
                        if len(roll_number_list) == 1 and roll_number_list[0].strip():
                            roll_numbers_str = (roll_number_list[0])
                            conditions = '("{}")'.format(roll_numbers_str)

                        else:
                           conditions = tuple(str(num) for num in roll_number_list)

                        query1 = f"DELETE FROM att_2024_04_20 WHERE roll_no IN {conditions}"
                        query2 = f"DELETE FROM registered_users WHERE roll_no IN {conditions}"
                        #print("q1,q2\n",query2,query1)
                        cursor.execute(query1)
                        connection.commit()
                        cursor.execute(query2)
                        connection.commit()
                        confirm_ent = Label(window, text="Delete Successful", font=("Arial", 25, 'bold'), fg="white",bg='green')
                        confirm_ent.place(x=490, y=610, width=500, height=60)

                    elif confirm_ent!="confirm":
                        confirm_ent = Label(window, text="Type 'confirm' to Delete the Above",font=("Arial", 25, 'bold'), fg="white", bg='red')
                        confirm_ent.place(x=490, y=610, width=500, height=60)
                    else:
                        confirm_ent = Label(window, text="Delete Failed",font=("Arial", 25, 'bold'), fg="white", bg='red')
                        confirm_ent.place(x=490, y=610, width=500, height=60)

                except:
                    confirm_ent = Label(window, text=f"Error in Deleting",font=("Arial", 25, 'bold'), fg="white", bg='red')
                    confirm_ent.place(x=490, y=610, width=500, height=60)

            next_btn = Button(window, text="DELETE", command=del_user,font=("Arial", 25, 'bold'))
            next_btn.place(x=486, y=764, width=520, height=47)


        def search_user():
            ent_label = Label(window, text="Search One Roll Number", font=("Arial", 25, 'bold'), fg="white",bg='green')
            ent_label.place(x=490, y=610, width=500, height=60)

            global query

            rfid_number_sr = rfid_numb_ent.get()
            roll_number_sr = roll_numb_ent.get()
            #name_ent = detail_ent.get()
            try:
                query_name = "SELECT name FROM registered_users WHERE "
                query_roll = "SELECT roll_no FROM registered_users WHERE "
                query_rfid_number = "SELECT rfid_number FROM registered_users WHERE "
                query_cat = "SELECT category FROM registered_users WHERE "
                conditions = []
                if rfid_number_sr:
                    conditions.append(f"rfid_number = '{rfid_number_sr}'")
                    query_cat = f"SELECT category FROM registered_users WHERE rfid_number = '{rfid_number_sr}'"
                if roll_number_sr:
                    conditions.append(f"roll_no = '{roll_number_sr}'")
                    query_cat = f"SELECT category FROM registered_users WHERE roll_no = '{roll_number_sr}'"
                query_name += "".join(conditions)
                query_roll += " AND ".join(conditions)
                query_rfid_number += "".join(conditions)


                cursor.execute(query_name)
                name_got = cursor.fetchall()

                cursor.execute(query_roll)
                roll_got = cursor.fetchall()

                cursor.execute(query_rfid_number)
                rfid_got = cursor.fetchall()

                cursor.execute(query_cat)
                cat_got = cursor.fetchall()

                connection.commit()
                search_label = Label(window, text=f"\nName:   {name_got[0][0]}\n\nRoll:   {roll_got[0][0]}\n\nRF No.:   {rfid_got[0][0]}\n\nCategory:   {cat_got[0][0]}\n", font=("Arial", 22, 'bold'),fg="white", bg='black', anchor="w", padx=15, pady=40)
                search_label.place(x=933, y=249, width=408, height=193)
                ent_label = Label(window, text="Search Done", font=("Arial", 25, 'bold'), fg="white", bg='green')
                ent_label.place(x=490, y=610, width=500, height=60)
            except:
                search_label = Label(window, text="\nName:\n\nRoll:\n\nRF No.:\n", font=("Arial", 27, 'bold'),fg="white", bg='black', anchor="w", padx=15, pady=40)
                search_label.place(x=933, y=249, width=408, height=193)
                ent_label = Label(window, text="Search Not found", font=("Arial", 25, 'bold'), fg="white",bg='red')
                ent_label.place(x=490, y=610, width=500, height=60)



        heading_label = Label(window, text="Update Panel", font=("Arial", 50, 'bold'), fg="#1d2f71", bg='#ad8140')
        rfid_number_label = Label(window, text="RFID Number:", font=("Arial", 30, 'bold'), fg="white", bg='#ad8140')
        roll_num_label = Label(window, text="Roll Number:", font=("Arial", 30, 'bold'), fg="white", bg='#ad8140')
        #ent_label = Label(window, text="Enter Label", font=("Arial", 30, 'bold'), fg="black", bg='lightblue')
        search_label = Label(window, text="\nName:\n\nRoll:\n\nRF No.:\n\nCategory:\n", font=("Arial", 22, 'bold'), fg="white", bg='black',anchor="w",padx=15, pady=40)

        up_name_btn = Button(window, text="Update\nName",font=("Arial", 20, 'bold'), fg="blue", bg='#ad8140',command=update_name)
        up_roll_btn = Button(window, text="Block\nUser",font=("Arial", 20, 'bold'), fg="blue", bg='#ad8140')
        del_user_btn = Button(window, text="Delete\nUser",font=("Arial", 20, 'bold'), fg="blue", bg='#ad8140',command=delete_user)
        search_btn = Button(window, text="Search\nUser",font=("Arial", 20, 'bold'), fg="blue", bg='#ad8140',command=search_user)
        scan_rf = Button(window, text="Scan",font=("Arial", 20, 'bold'), fg="blue", bg='black')


        #rfid_numb_ent = Label(window, font=("Arial", 25, 'bold'), fg="#ad8140", bg='black')
        rfid_numb_ent = Entry(window,font=("Arial", 25, 'bold'),fg="#ad8140", bg='black')
        roll_numb_ent = Entry(window,font=("Arial", 25, 'bold'),fg="#ad8140", bg='black')
        detail_ent = Entry(window,font=("Arial", 25, 'bold'),fg="#ad8140", bg='black')


        heading_label.place(x=142, y=49, width=1155, height=131)
        rfid_number_label.place(x=158, y=286, width=226, height=59)
        roll_num_label.place(x=158, y=380, width=226, height=59)

        #ent_label.place(x=490, y=610, width=500, height=60)
        search_label.place(x=933, y=249, width=408, height=193)

        up_roll_btn.place(x=486, y=498, width=217, height=86)
        up_name_btn.place(x=207, y=498, width=217, height=86)
        del_user_btn.place(x=773, y=498, width=217, height=86)
        search_btn.place(x=1080, y=498, width=217, height=86)
        scan_rf.place(x=702, y=285, width=146, height=59)


        rfid_numb_ent.place(x=424, y=285, width=226, height=59)
        roll_numb_ent.place(x=424, y=380, width=424, height=59)
        detail_ent.place(x=532, y=683, width=424, height=59)




    # attendance
    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: attendance_menu(),
        relief="flat"
    )
    button_3.place(
        x=189.0,
        y=363.0,
        width=383.0,
        height=105.0
    )

    # print
    button_image_4 = PhotoImage(
        file=relative_to_assets("button_4.png"))
    button_4 = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("print clicked"),
        relief="flat"
    )
    button_4.place(
        x=842.0,
        y=518.0,
        width=383.0,
        height=105.0
    )
    # search
    button_image_5 = PhotoImage(
        file=relative_to_assets("button_rf.png"))
    button_5 = Button(
        image=button_image_5,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("search clicked"),
        relief="flat"
    )
    button_5.place(
        x=191.0,
        y=673.0,
        width=383.0,
        height=105.0
    )
    #update print("update clicked")
    button_image_6 = PhotoImage(
        file=relative_to_assets("button_6.png"))
    button_6 = Button(
        image=button_image_6,
        borderwidth=0,
        highlightthickness=0,
        command=lambda:update_panel(),
        relief="flat"
    )

    button_6.place(
        x=842.0,
        y=673.0,
        width=383.0,
        height=105.0
    )
    # view att
    button_image_7 = PhotoImage(
        file=relative_to_assets("button_7.png"))
    button_7 = Button(
        image=button_image_7,
        borderwidth=0,
        highlightthickness=0,
        command=view_panel,
        relief="flat"
    )
    button_7.place(
        x=189.0,
        y=518.0,
        width=383.0,
        height=105.0
    )

    # register
    button_image_8 = PhotoImage(
        file=relative_to_assets("button_8.png"))
    button_8 = Button(
        image=button_image_8,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: register_menu(),
        relief="flat"
    )
    button_8.place(
        x=842.0,
        y=363.0,
        width=383.0,
        height=105.0
    )
    my_font = ('times', 50, 'bold')
    l1 = Button(window, font=my_font, borderwidth=0,
                highlightthickness=0, bg="#ad81ff", fg="#ad8140")
    l1.place(x=412.0,
             y=244.0,
             width=595.0,
             height=86.0)
    def on_key_press(event):
        if event.keysym == "Escape":
            rerun_program()

    my_time()
    window.bind("<Key>", on_key_press)
    window.resizable(True, True)
    # Create an MQTT client instance
    """client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)

    # Set the on_connect and on_message callback functions
    #client.on_connect = on_connect
    #client.on_message = on_message

    # Set the username and password for connecting to the MQTT broker
    client.username_pw_set(username, password)
    client.connect(broker_address, 18731, 60)

    # Define a function to start the MQTT client loop in a separate thread
    def start_mqtt_loop():
        client.loop_forever()

    # Start the MQTT client loop in a separate thread
    mqtt_thread = threading.Thread(target=start_mqtt_loop)
    mqtt_thread.start()"""
    window.mainloop()


main()


