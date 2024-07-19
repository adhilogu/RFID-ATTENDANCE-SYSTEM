from pathlib import Path
import os
import time
from datetime import date
import pymysql
from tkinter import *
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage,ttk
from tkinter import ttk
from tkcalendar import DateEntry
import datetime
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import threading
#import serial

from babel import numbers
import sqlite3
from tkinter import messagebox
from tkinter import filedialog


# ser = serial.Serial('COM5', 9600)  # Update with correct port

connection = sqlite3.connect('attendance_system.db')
cursor = connection.cursor()

OUTPUT_PATH = Path(__file__).parent
#ASSETS_PATH = OUTPUT_PATH / Path(r"build\assets\frame0")
ASSETS_PATH = OUTPUT_PATH / Path(r"/Users/adhilogu2004gmail.com/Downloads/frame1")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()
window.title('ATTENDANCE SYSTEM')
window.geometry("1450x950")
window.attributes('-fullscreen', False)
#width = window.winfo_screenwidth()

#height = window.winfo_screenheight()
#print(f"width = {width}, height = {height}")
global l1, button_1,button_2,button_3,button_4,button_5,button_6,button_7,button_8,my_font,rows
global scan_rfid,thread
my_font = ('times', 40, 'bold')
def my_time():
    time_string = time.strftime('%I:%M:%S %p / %d-%m-%Y')
    l1.config(text=time_string)
    l1.after(1000, my_time)


def login():
    # button_1.place_forget()
    # global button_1,button_2,button_3,button_4,button_5,button_6,button_7,button_8,l1
    #global window
    global password_entry
    status1.place_forget()
    #name_label.place_forget()
    #name_entry.place_forget()
    #search_button.place_forget()
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
    #status1.place_forget()



    def check_user():
        global password_entry
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
                home()
            else:
                # messagebox.showerror("Error", "Invalid username or password")
                down_label = Label(window, text="Invalid username or password", bg="red", fg="white",
                                   font=("Arial", 30, 'bold'))
                down_label.place(x=329.0, y=727.0, width=809.0, height=59.0)
        except Exception as e:
            down_label = Label(window, text=f"An error occurred: {str(e)}", bg="red", fg="white",
                               font=("Arial", 30, 'bold'))
            down_label.place(x=329.0, y=727.0, width=809.0, height=59.0)


    password_label = Label(window, text="Password:",font=("Arial", 32,'bold'), bg="#013f95", fg='white')
    password_label.place(x=485.0, y=485.0, width=226.0, height=59.0)
    password_entry = Entry(window, show="*",font=("Arial", 40,'bold'), fg="#013f95",bg="white",insertbackground='red')
    password_entry.place(x=741.0, y=485.0, width=226.0, height=59.0)
    user_label = Label(window, text="User:", font=("Arial", 35,'bold'), bg="#013f95", fg='white')
    user_label.place(x=485.0, y=391.0, width=226.0, height=59.0)

    # Create a dropdown for user selection
    user_var = StringVar(window)
    user_var.set("admin")  # Default selection
    user_dropdown = OptionMenu(window, user_var, "adhi","admin", "student")
    user_dropdown.config(font=("Arial", 20,'bold'), fg="#013f95",bg="white")
    user_dropdown.place(x=741.0, y=391.0, width=226.0, height=59.0)

    # Create a button to login
    login_button = Button(window, text="Login", command=check_user,fg="#1d2f71", font=("Arial", 25,'bold'))
    login_button.place(x=491.0, y=599.0, width=466.0, height=47.0)
    password_entry.focus_set()
    def on_key_press(key):
        try:
            # Check if the key is alphanumeric
            if key.keysym == "Return":
                login_button.invoke()
        except Exception as e:
            print(e)

    window.bind("<Key>", on_key_press)
    window.mainloop()


def update_panel():
    global button_image_1, ltime, Canvas, canvas, next_btn, rfid_numb_ent
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
                ent_label = Label(window, text="Enter Any One RF No./Roll No.", font=("Arial", 25, 'bold'), fg="white",
                                  bg='red')
                ent_label.place(x=490, y=610, width=500, height=60)
                return

            try:
                query = f"UPDATE registered_users SET name ='{name_ent}' WHERE "
                conditions = []
                if rfid_number_up and name_ent:
                    conditions.append(f"rfid_number = '{rfid_number_up}'")
                    ent_label = Label(window, text=f"Updated {rfid_number_up}'s Name {name_ent}",
                                      font=("Arial", 25, 'bold'), fg="white", bg='green')
                    ent_label.place(x=490, y=610, width=500, height=60)
                    query += "".join(conditions)
                elif roll_number_up and name_ent:
                    conditions.append(f"roll_no = '{roll_number_up}'")
                    ent_label = Label(window, text=f"Updated {roll_number_up}'s Name {name_ent}",
                                      font=("Arial", 25, 'bold'), fg="white", bg='green')
                    ent_label.place(x=490, y=610, width=500, height=60)
                    query += "".join(conditions)

                else:
                    ent_label = Label(window, text="Enter RF No./Roll No. & New Name", font=("Arial", 25, 'bold'),
                                      fg="white", bg='red')
                    ent_label.place(x=490, y=610, width=500, height=60)


            except:
                ent_label = Label(window, text=f"Error in Updating", font=("Arial", 25, 'bold'), fg="white", bg='red')
                ent_label.place(x=490, y=610, width=500, height=60)
            cursor.execute(query)
            connection.commit()

        next_btn = Button(window, text="UPDATE", command=upd_name, font=("Arial", 25, 'bold'))
        next_btn.place(x=486, y=764, width=520, height=47)

    def delete_user():
        ent_label = Label(window, text="Enter the Roll Number(s) to Delete", font=("Arial", 25, 'bold'), fg="white",
                          bg='green')
        ent_label.place(x=490, y=610, width=500, height=60)

        def del_user():
            global query1, query2
            rfid_number_del = rfid_numb_ent.get()
            roll_number_del = roll_numb_ent.get()
            confirm_ent = detail_ent.get()

            if not roll_number_del:
                confirm_ent = Label(window, text="Entry Roll Number(s)", font=("Arial", 25, 'bold'), fg="white",
                                    bg='red')
                confirm_ent.place(x=490, y=610, width=500, height=60)
                return
            try:
                if roll_number_del and confirm_ent == "confirm":

                    roll_number_list = roll_number_del.split(',')
                    if len(roll_number_list) == 1 and roll_number_list[0].strip():
                        roll_numbers_str = (roll_number_list[0])
                        conditions = '("{}")'.format(roll_numbers_str)

                    else:
                        conditions = tuple(str(num) for num in roll_number_list)

                    query1 = f"DELETE FROM att_2024_04_20 WHERE roll_no IN {conditions}"
                    query2 = f"DELETE FROM registered_users WHERE roll_no IN {conditions}"
                    # print("q1,q2\n",query2,query1)
                    cursor.execute(query1)
                    connection.commit()
                    cursor.execute(query2)
                    connection.commit()
                    confirm_ent = Label(window, text="Delete Successful", font=("Arial", 25, 'bold'), fg="white",
                                        bg='green')
                    confirm_ent.place(x=490, y=610, width=500, height=60)

                elif confirm_ent != "confirm":
                    confirm_ent = Label(window, text="Type 'confirm' to Delete the Above", font=("Arial", 25, 'bold'),
                                        fg="white", bg='red')
                    confirm_ent.place(x=490, y=610, width=500, height=60)
                else:
                    confirm_ent = Label(window, text="Delete Failed", font=("Arial", 25, 'bold'), fg="white", bg='red')
                    confirm_ent.place(x=490, y=610, width=500, height=60)

            except:
                confirm_ent = Label(window, text=f"Error in Deleting", font=("Arial", 25, 'bold'), fg="white", bg='red')
                confirm_ent.place(x=490, y=610, width=500, height=60)

        next_btn = Button(window, text="DELETE", command=del_user, font=("Arial", 25, 'bold'))
        next_btn.place(x=486, y=764, width=520, height=47)

    def scan_butn_reg():
        global rfid_numb_ent
        rfid_numb_ent.delete(0, "end")
        rfid_numb_ent.focus_set()

    def search_user():
        ent_label = Label(window, text="Search One Roll Number", font=("Arial", 25, 'bold'), fg="white", bg='green')
        ent_label.place(x=490, y=610, width=500, height=60)

        global query

        rfid_number_sr = rfid_numb_ent.get()
        roll_number_sr = roll_numb_ent.get()
        # name_ent = detail_ent.get()
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
            search_label = Label(window,
                                 text=f"\nName:   {name_got[0][0]}\n\nRoll:   {roll_got[0][0]}\n\nRF No.:   {rfid_got[0][0]}\n\nCategory:   {cat_got[0][0]}\n",
                                 font=("Arial", 17, 'bold'), fg="white", bg='black', anchor="w", padx=15, pady=40)
            search_label.place(x=933, y=249, width=408, height=193)
            ent_label = Label(window, text="Search Done", font=("Arial", 25, 'bold'), fg="white", bg='green')
            ent_label.place(x=490, y=610, width=500, height=60)
        except:
            search_label = Label(window, text="\nName:\n\nRoll:\n\nRF No.:\n", font=("Arial", 17, 'bold'), fg="white",
                                 bg='black', anchor="w", padx=15, pady=40)
            search_label.place(x=933, y=249, width=408, height=193)
            ent_label = Label(window, text="Search Not found", font=("Arial", 25, 'bold'), fg="white", bg='red')
            ent_label.place(x=490, y=610, width=500, height=60)





    heading_label = Label(window, text="Update Panel", font=("Arial", 50, 'bold'), fg="white", bg='#070c40')
    rfid_number_label = Label(window, text="RFID Number:", font=("Arial", 25, 'bold'), bg="#013f95", fg='white')
    roll_num_label = Label(window, text="Roll Number:", font=("Arial", 25, 'bold'), bg="#013f95", fg='white')
    # ent_label = Label(window, text="Enter Label", font=("Arial", 30, 'bold'), fg="black", bg='lightblue')
    search_label = Label(window, text="\nName:\n\nRoll:\n\nRF No.:\n\nCategory:\n", font=("Arial", 17, 'bold'),
                         fg="white", bg='black', anchor="w", padx=15, pady=40)

    up_name_btn = Button(window, text="Update\nName", font=("Arial", 20, 'bold'), bg="white", fg='#013f95',
                         command=update_name)
    up_roll_btn = Button(window, text="Block\nUser", font=("Arial", 20, 'bold'), bg="white", fg='#013f95')
    del_user_btn = Button(window, text="Delete\nUser", font=("Arial", 20, 'bold'), bg="white", fg='#013f95',
                          command=delete_user)
    search_btn = Button(window, text="Search\nUser", font=("Arial", 20, 'bold'), bg="white", fg='#013f95',
                        command=search_user)
    scan_rf = Button(window, text="Scan", font=("Arial", 20, 'bold'),command=scan_butn_reg, fg="blue", bg='white')

    # rfid_numb_ent = Label(window, font=("Arial", 25, 'bold'), fg="#ad8140", bg='black')
    rfid_numb_ent = Entry(window, font=("Arial", 22, 'bold'), fg="#013f95", bg='white')
    roll_numb_ent = Entry(window, font=("Arial", 22, 'bold'), fg="#013f95", bg='white')
    detail_ent = Entry(window, font=("Arial", 25, 'bold'), fg="#013f95", bg='white')

    heading_label.place(x=142, y=49, width=1155, height=131)
    rfid_number_label.place(x=158, y=286, width=226, height=59)
    roll_num_label.place(x=158, y=380, width=226, height=59)

    # ent_label.place(x=490, y=610, width=500, height=60)
    search_label.place(x=933, y=249, width=408, height=193)

    up_roll_btn.place(x=486, y=498, width=217, height=86)
    up_name_btn.place(x=207, y=498, width=217, height=86)
    del_user_btn.place(x=773, y=498, width=217, height=86)
    search_btn.place(x=1080, y=498, width=217, height=86)
    scan_rf.place(x=702, y=285, width=146, height=59)

    rfid_numb_ent.place(x=424, y=285, width=226, height=59)
    roll_numb_ent.place(x=424, y=380, width=424, height=59)
    detail_ent.place(x=532, y=683, width=424, height=59)


    window.mainloop()


def attendance_menu():
    global button_image_1, ltime, name_label, name_entry, search_button, roll_number_label, attendance_table, status1, name_of_roll

    # Hide the initial buttons
    button_1.place_forget()
    button_2.place_forget()
    button_3.place_forget()
    button_4.place_forget()
    button_5.place_forget()
    button_6.place_forget()
    button_7.place_forget()
    button_8.place_forget()
    l1.place_forget()

    my_font = ('times', 40, 'bold')

    # Initialize the rfid_data list
    rfid_data = []

    def on_key_press(key):
        nonlocal rfid_data
        try:
            # Check if the key is alphanumeric
            if key.keysym == "Escape":
                login()


            if key.char.isalnum():
                if len(rfid_data) == 0:
                    rfid_data = []
                    print("cleared")
                    rfid_data.clear()
                    rfid_data.clear()
                rfid_data.append(key.char)
                if len(rfid_data) == 10:

                    rf_join_data = ''.join(rfid_data)
                    current_atte(rf_join_data)
                    print("rfid", rf_join_data)
                    rfid_data.clear()
                    rfid_data.clear()
                    update_attendance_table()
        except Exception as e:
            print(e)
            # Special keys (like Ctrl, Alt, etc.) will raise an AttributeError as they do not have 'char' attribute
            #pass

    def current_atte(rfid_number):
        connection = sqlite3.connect('attendance_system.db')
        cursor = connection.cursor()
        global status1, name_of_roll

        cursor.execute("SELECT roll_no FROM registered_users WHERE rfid_number = ?", (rfid_number,))
        result = cursor.fetchone()

        if result:
            cursor.execute("SELECT name FROM registered_users WHERE rfid_number = ?", (rfid_number,))
            name_of = cursor.fetchone()
            if name_of:
                name_of_roll = name_of[0].upper()
            cursor.execute("INSERT INTO att_2024_04_20 (rfid, roll_no) VALUES (?, ?)", (rfid_number, result[0]))
            roll_number_label.config(text=f"{result[0]}\n{name_of_roll}")
            status1 = Label(window, text="PRESENT", font=my_font, borderwidth=0,
                            highlightthickness=0, bg="green", fg="white")
            status1.place(x=733.0, y=700.0, width=610.0, height=100.0)
            update_attendance_table()
            connection.commit()
        else:
            roll_number_label.config(text=f"Unknown - {rfid_number}")
            status1 = Label(window, text="UNKNOWN", font=my_font, borderwidth=0,
                            highlightthickness=0, bg="red", fg="white")
            status1.place(x=733.0, y=700.0, width=610.0, height=100.0)
        #roll_number_label.config(text="")

        connection.close()

    status1 = Label(window, text="UNKNOWN", font=my_font, borderwidth=0,
                    highlightthickness=0, bg="red", fg="white")

    def update_attendance_table():
        connection = sqlite3.connect('attendance_system.db')
        cursor = connection.cursor()

        cursor.execute("select * from att_2024_04_20 where date(timestamp)=date('now')")
        data = cursor.fetchall()

        for row in attendance_table.get_children():
            attendance_table.delete(row)
        for record in data:
            attendance_table.insert('', 'end', text=record[0], values=record[1:3])
        connection.close()

    ltime = Button(window, font=my_font, borderwidth=0, highlightthickness=0, bg="#013f95", fg="white")
    ltime.place(x=740.0, y=330.0, width=595.0, height=86.0)

    attendance_table = ttk.Treeview(window, columns=("Time Stamp", "Roll Number", "Roll"))
    style = ttk.Style()
    style.theme_use('default')
    attendance_table.heading("#0", text="RFID")
    attendance_table.column("#0", anchor=CENTER, stretch=NO, width=200)
    attendance_table.heading("Time Stamp", text="Time Stamp")
    attendance_table.heading("Roll Number", text="Roll Number")
    attendance_table.column("#2", anchor=CENTER, stretch=NO, width=200)
    attendance_table.heading("Roll", text="Roll")
    attendance_table.column("#3", anchor=CENTER, stretch=NO, width=200)

    attendance_table.place(x=70, y=325, width=600.0, height=552.0)

    roll_number_label = Label(window, text="Next", font=my_font, borderwidth=0,highlightthickness=0, bg="#070c40", fg="white")


    roll_number_label.place(x=733.0, y=527.0, width=610.0, height=150.0)

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
    window.bind("<Key>", on_key_press)
    my_time_2()
    update_attendance_table()
    #listener = keyboard.Listener(on_press=on_key_press)
    #listener.start()
    window.mainloop()

def view_panel():  #######viewwwwwww----------------------------
    # hide the existing buttons
    button_1.place_forget()
    button_2.place_forget()
    button_3.place_forget()
    button_4.place_forget()
    button_5.place_forget()
    button_6.place_forget()
    button_7.place_forget()
    button_8.place_forget()
    l1.place_forget()
    global button_image_1, ltime, Canvas, canvas, numbers, rfid_number_entry

    rfid_number_entry = Entry(window, font=("Arial", 25, 'bold'), bg="#013f95", fg='white')


    def select_from_date(event=None):
        global selected_from_date
        selected_from_date = from_date_entry_date.get_date()
        from_date_entry.config(text=f"{selected_from_date}")

    def select_to_date(event=None):
        global selected_to_date
        selected_to_date = to_date_entry_date.get_date()
        to_date_entry.config(text=f"{selected_to_date}")

    def today_data():
        cursor.execute("select * from att_2024_04_20 where date(timestamp)=date('now') ")
        #cursor.execute("select * from att_2024_04_20 ")
        rows = cursor.fetchall()

        table.delete(*table.get_children())

        # Insert fetched data into the Treeview widget
        for i, row in enumerate(rows, start=1):
            table.insert('', 'end', text=row[0], values=row[1:5])
            #print(rows)

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

        # table.place(x=75, y=190, width=615.0, heigh=520.0)

        hello_label = Label(window, text="Today's Attendance", bg="green", font=("Arial", 17))
        hello_label.place(x=813, y=150, width=600, height=75)
        connection.commit()

    def scan_butn_reg():
        global rfid_number_entry,roll_number_entry,month_entry
        rfid_number_entry.delete(0, "end")
        roll_number_entry.delete(0, "end")
        month_entry.delete(0, "end")
        rfid_number_entry.focus_set()

    def reset_quick_att_data():
        cursor.execute("delete FROM quick_att") #att_2024_04_20
        connection.commit()
        hello_label = Label(window, text="Quick Attendance Deleted", bg="green", fg="red", font=("Arial", 17))
        hello_label.place(x=813, y=150, width=600, height=75)

    def quick_att_data():
        global rows, headers
        global canvas
        cursor.execute("SELECT DISTINCT name,roll_no,rfid  FROM quick_att")

        rows = cursor.fetchall()

        table.delete(*table.get_children())

        # Insert fetched data into the Treeview widget
        for i, row in enumerate(rows, start=1):
            table.insert('', 'end', text=row[0], values=row[1:5])
            #print(rows)

        # Close the cursor and connection

        table.heading("#0", text="Name")
        table.heading("#1", text="Roll Number")
        table.heading("#2", text="RFID")
        # table.heading("#3", text="RFID-Number")
        # table.heading("#4", text="Time Stamp")

        headers = ["Name", "Roll Number", "RFID"]
        # columns = ("Name", "Time Stamp", "Roll Number", "RF Number"))
        # Define column widths
        table.column("#0", anchor="center", width=150)
        table.column("#1", anchor="center", width=180)
        table.column("#2", anchor="center", width=180)
        # table.column("#3", anchor="center", width=190)
        # table.column("#4", anchor="center", width=150)

        # table.place(x=75, y=190, width=615.0, heigh=520.0)

        hello_label = Label(window, text="Quick Attendance", bg="green", font=("Arial", 17))
        hello_label.place(x=813, y=150, width=600, height=75)
        connection.commit()

    def view_data():
        global canvas, rfid_number_entry,thread
        # Get values from entry widgets
        global rows, headers, query
        rfid_number = rfid_number_entry.get()
        roll_number = roll_number_entry.get()
        month = month_entry.get()


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
            hello_label = Label(window, text="TWO REQUIREMENTS NEEDED (ENTER DATE)", bg="red", font=("Arial", 17))
            hello_label.place(x=813, y=150, width=600, height=75)

        # Execute the query

        cursor.execute(query)
        rows = cursor.fetchall()

        table.delete(*table.get_children())

        # Insert fetched data into the Treeview widget
        for i, row in enumerate(rows, start=1):
            table.insert('', 'end', text=row[0], values=row[1:5])
            # print(rows)

        # Close the cursor and connection

        table.heading("#0", text="ID")
        table.heading("#1", text="RFID-Number")
        table.heading("#2", text="Time Stamp")
        table.heading("#3", text="Roll Number")
        table.heading("#4", text="Category")

        headers = ["ID", "RFID-Number", "Time Stamp", "Roll Number", "Category"]

        # Define column widths
        table.column("#0", anchor="center", width=80)
        table.column("#1", anchor="center", width=180)
        table.column("#2", anchor="center", width=180)
        table.column("#3", anchor="center", width=190)

        # table.place(x=75, y=190, width=615.0, heigh=520.0)

        hello_label = Label(window, text="Search Done", bg="green", font=("Arial", 17))
        hello_label.place(x=813, y=150, width=600, height=75)

    def calculate_working_hours():
        global rows, headers

        roll_number = roll_number_entry.get()
        rfid_number = rfid_number_entry.get()
        try:
            if (not roll_number) and (not rfid_number):
                cursor.execute("""SELECT 
                                a.rfid,
                                r.name AS Name,
                                strftime('%H hours %M minutes', 
                                         JULIANDAY(MAX(a.timestamp)) - JULIANDAY(MIN(a.timestamp))) 
                                         AS Total_Working_Hours
                            FROM 
                                att_2024_04_20 AS a
                            JOIN 
                                registered_users AS r ON a.rfid = r.rfid_number
                            GROUP BY 
                                a.rfid, r.name;""")
                print("1")




            elif rfid_number:
                rfid_numbers_st = rfid_number.split(',')
                if len(rfid_numbers_st) == 1 and rfid_numbers_st[0].strip():
                    rfid_numbers_str = (rfid_numbers_st[0])
                    rfid_numbers_str = '("{}")'.format(rfid_numbers_str)


                else:
                    rfid_numbers_str = tuple(rfid_numbers_st)
                sql_query = f"""SELECT 
                                a.rfid,
                                r.name AS Name,
                                strftime('%H hours %M minutes', 
                                         JULIANDAY(MAX(a.timestamp)) - JULIANDAY(MIN(a.timestamp))) 
                                         AS Total_Working_Hours
                            FROM 
                                att_2024_04_20 AS a
                            JOIN 
                                registered_users AS r ON a.rfid = r.rfid_number
                            WHERE 
                                a.rfid IN ({rfid_numbers_str})
                            GROUP BY 
                                a.rfid, r.name;
                                                """

                # Execute the SQL query with roll_numbers_str as parameter
                #print("\nrfstr", rfid_numbers_str)
                cursor.execute(sql_query)
                print("2")

            if rfid_number and selected_to_date and selected_from_date:
                rfid_numbers_st = rfid_number.split(',')
                if len(rfid_numbers_st) == 1 and rfid_numbers_st[0].strip():
                    rfid_numbers_str = (rfid_numbers_st[0])
                    rfid_numbers_str = '("{}")'.format(rfid_numbers_str)
                else:
                    rfid_numbers_str = tuple(rfid_numbers_st)

                # Ensure selected_to_date and selected_from_date are properly formatted
                #selected_to_date_str = selected_to_date.get_date()
                #selected_from_date_str = selected_from_date.get_date()
                print(f"{selected_to_date}------{selected_from_date}")

                sql_query = f"""SELECT 
                                a.rfid,
                                r.name AS Name,
                                strftime('%H hours %M minutes', 
                                         JULIANDAY(MAX(a.timestamp)) - JULIANDAY(MIN(a.timestamp))) 
                                         AS Total_Working_Hours
                            FROM 
                                att_2024_04_20 AS a
                            JOIN 
                                registered_users AS r ON a.rfid = r.rfid_number
                            WHERE 
                                a.rfid IN ({rfid_numbers_str})
                                AND a.timestamp BETWEEN '{selected_from_date}' AND '{selected_to_date}'
                            GROUP BY 
                                a.rfid, r.name;
                                            """

                cursor.execute(sql_query)
                print("4")


            elif roll_number:

                roll_numbers_st = roll_number.split(',')
                if len(roll_numbers_st) == 1 and roll_numbers_st[0].strip():
                    roll_numbers_str = (roll_numbers_st[0])
                    roll_numbers_str = '("{}")'.format(roll_numbers_str)

                else:
                    roll_numbers_str = tuple(roll_numbers_st)

                sql_query = f"""SELECT 
                                a.rfid,
                                r.name AS Name,
                                strftime('%H hours %M minutes', 
                                         JULIANDAY(MAX(a.timestamp)) - JULIANDAY(MIN(a.timestamp))) 
                                         AS Total_Working_Hours
                            FROM 
                                att_2024_04_20 AS a
                            JOIN 
                                registered_users AS r ON a.rfid = r.rfid_number
                            WHERE 
                                a.roll_no IN ({roll_numbers_str})
                            GROUP BY 
                                a.rfid, r.name;
                                                """

                # Execute the SQL query with roll_numbers_str as parameter

                cursor.execute(sql_query)
                print("3")


            rows = cursor.fetchall()

            table.delete(*table.get_children())
            for i, row in enumerate(rows, start=1):
                table.insert('', 'end', text=row[0], values=row[1:4])
                #1print(rows)

            table.heading("#0", text="Roll Number")
            table.heading("#1", text="Name")
            table.heading("#2", text="Total Working Hours")

            headers = ["Roll Number", "Name", "Total Working Hours"]
            # Define column widths
            table.column("#0", anchor="center", width=190)
            table.column("#1", anchor="center", width=190)
            table.column("#2", anchor="center", width=180)

            # table.place(x=75, y=190, width=615.0, heigh=520.0)
            hello_label = Label(window, text=f"Working Hours", bg="green", font=("Arial", 17))
            hello_label.place(x=813, y=150, width=600, height=75)
        except Exception as e:
            #hello_label = Label(window, text=f"Error in Hours Search (Enter Date) {e}", bg="red", font=("Arial", 20))
            hello_label = Label(window, text=f"Er  {e}", bg="red", font=("Arial", 17))
            hello_label.place(x=813, y=150, width=600, height=75)

    logolabel = Label(window, text="VIEW PANEL", font=("Arial", 40, 'bold'), bg="#013f95", fg='white')
    logolabel.place(x=86, y=26, width=1294, height=83)

    def clear_table():

        table.delete(*table.get_children())
        rfid_number_entry.delete(0, "end")
        roll_number_entry.delete(0, "end")
        month_entry.delete(0, "end")


        hello_label = Label(window, text="Search", bg="#070c40", fg="white", font=("Arial", 32, 'bold'))
        hello_label.place(x=813, y=150, width=600, height=75)

    def display_registered_users():
        # Execute the SQL query to fetch all data from registered_users table
        global rows, headers, rfid_number_entry
        global canvas
        try:
            cursor.execute("SELECT * FROM registered_users")

            # Fetch all rows from the result set
            rows = cursor.fetchall()

            table.delete(*table.get_children())

            # Insert fetched data into the Treeview widget
            for i, row in enumerate(rows, start=1):
                table.insert('', 'end', text=row[0], values=row[1:5])
                #print(rows)

            table.heading("#0", text="Name")
            table.heading("#1", text="Roll Number")
            table.heading("#2", text="RF Number")
            table.heading("#3", text="Category")
            #table.heading("#4", text="Category")

            headers = ["Name", "Roll Number", "RF Number", "Category"]

            # Define column widths
            table.column("#0", anchor="center", width=180)
            table.column("#1", anchor="center", width=180)
            table.column("#2", anchor="center", width=180)
            table.column("#3", anchor="center", width=190)
            #table.column("#4", anchor="center", width=100)

            # table.place(x=75, y=190, width=615.0, heigh=520.0)
            hello_label = Label(window, text="All Students", bg="green", font=("Arial", 17))
            hello_label.place(x=813, y=150, width=600, height=75)

        except:
            hello_label = Label(window, text="ERROR IN USER TABLE", bg="red", font=("Arial", 17))
            hello_label.place(x=813, y=150, width=600, height=75)



    def present_usr():
        table.delete(*table.get_children())
        try:
            cursor.execute(
                f"SELECT DISTINCT ru.name, ru.roll_no FROM registered_users ru JOIN att_2024_04_20 a ON ru.roll_no = a.roll_no WHERE DATE(a.timestamp) BETWEEN '{selected_from_date}' AND '{selected_to_date}'")

            # Fetch all rows from the result set
            rows = cursor.fetchall()

            table.delete(*table.get_children())

            # Insert fetched data into the Treeview widget
            for i, row in enumerate(rows, start=1):
                table.insert('', 'end', text=row[0], values=row[1:5])
                # print(rows)

            table.heading("#0", text="Name")
            table.heading("#1", text="Roll Number")

            headers = ["Name", "Roll Number"]

            # Define column widths
            table.column("#0", anchor="center", width=200)
            table.column("#1", anchor="center", width=200)

            table.place(x=75, y=190, width=615.0, heigh=637.0)
            hello_label = Label(window, text=f"Present Students {selected_from_date} - {selected_to_date}", bg="green",
                                font=("Arial", 20))
            hello_label.place(x=813, y=150, width=600, height=75)

        except:
            hello_label = Label(window, text="ENTER FROM AND TO", bg="red", font=("Arial", 17))
            hello_label.place(x=813, y=150, width=600, height=75)

    def generate_pdf():
        global canvas
        try:
            downloads_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

            # Construct the filename with the timestamp
            # filename = f"table_data_{timestamp}.pdf"
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
            hello_label = Label(window, text=f"PDF CREATED SUCCESSFULLY \n table_data_{timestamp}.pdf", bg="green",
                                font=("Arial", 17))
            hello_label.place(x=813, y=150, width=600, height=75)

        except Exception as e:
            print("An error occurred:", e)
            hello_label = Label(window, text=f"PDF CREATED UNSUCCESSFULL \n {e}", bg="red", font=("Arial", 17))
            hello_label.place(x=813, y=150, width=600, height=75)

    # Create buttons with individual styles
    table = ttk.Treeview(window, columns=("Name", "Roll Number", "RF Number", "Time Stamp"))
    # Create an instance of Style widget
    style = ttk.Style()
    style.theme_use('default')

    scan_button = Button(window, text="Scan", fg="#1d2f71", font=("Arial", 20, 'bold'),command=scan_butn_reg)

    roll_number_entry = Entry(window, font=("Arial", 25, 'bold'), bg="white", fg='black', insertbackground='#013f95')
    from_date_entry = Label(window, text="FROM", font=("Arial", 20, 'bold'), bg="#013f95", fg='white')
    to_date_entry = Label(window, text="TO", font=("Arial", 20, 'bold'), bg="#013f95", fg='white')
    month_entry = Entry(window, font=("Arial", 25, 'bold'), bg="white", fg='black', insertbackground='#013f95')
    table.place(x=75, y=190, width=615.0, heigh=520.0)

    from_date_entry_date = DateEntry(window, width=12, insertbackground='#013f95')
    from_date_entry_date.place(x=1043, y=460, width=157, height=25)

    to_date_entry_date = DateEntry(window, width=12, insertbackground='#013f95')
    to_date_entry_date.place(x=1232, y=460, width=157, height=25)

    from_date_entry_date.bind("<<DateEntrySelected>>", select_from_date)
    to_date_entry_date.bind("<<DateEntrySelected>>", select_to_date)

    view_button = Button(window, text="View", font=("Arial", 40, 'bold'),  bg="white", fg='#013f95', command=view_data)
    time_spent_button = Button(window, text="Time Spent", font=("Arial", 20, 'bold'),  bg="white", fg='#013f95',
                               command=calculate_working_hours)
    today_button = Button(window, text="Today", font=("Arial", 25, 'bold'),  bg="white", fg='#013f95',
                          command=today_data)
    # check_button = Button(window, text="Check",  font=("Arial", 25, 'bold'), fg="#1d2f71",bg='#1d2f71')
    students_button = Button(window, text="Students", font=("Arial", 25, 'bold'),  bg="white", fg='#013f95',
                             command=display_registered_users)
    print_button = Button(window, text="Print", font=("Arial", 25, 'bold'), bg="white", fg='#013f95',
                          command=generate_pdf)
    clear_button = Button(window, text="Clear", font=("Arial", 25, 'bold'), bg="white", fg='#013f95',
                          command=clear_table)
    ab_button = Button(window, text="Ab", font=("Arial", 25, 'bold'), bg="white", fg='#013f95')
    pr_button = Button(window, text="Pr", font=("Arial", 25, 'bold'), bg="white", fg='#013f95', command=present_usr)
    quick_att_btn = Button(window, text="Quick Att", font=("Arial", 25, 'bold'), bg="white", fg='#013f95',
                           command=quick_att_data)
    reset_quick_att_btn = Button(window, text="Reset Quick Att", font=("Arial", 15, 'bold'), bg="white", fg='#013f95',command=reset_quick_att_data)

    # Create labels
    rfid_number_label = Label(window, text="RFID Number", font=("Arial", 22, 'bold'), bg="#013f95", fg='white')
    roll_number_label = Label(window, text="Roll Number(s)", font=("Arial", 22, 'bold'), bg="#013f95", fg='white')
    date_label = Label(window, text="Date", font=("Arial", 30, 'bold'), bg="#013f95", fg='white')
    month_label = Label(window, text="Month", font=("Arial", 30, 'bold'), bg="#013f95", fg='white')

    # Place labels
    rfid_number_label.place(x=813, y=268, width=197, height=47)
    roll_number_label.place(x=813, y=369, width=205, height=47)
    date_label.place(x=813, y=470, width=197, height=47)
    month_label.place(x=813, y=571, width=197, height=47)

    # Place buttons
    view_button.place(x=823, y=638, width=566, height=47)
    time_spent_button.place(x=823, y=713, width=157, height=47)
    today_button.place(x=823, y=777, width=157, height=47)
    ab_button.place(x=1039, y=713, width=75, height=47)
    pr_button.place(x=1119, y=713, width=75, height=47)
    students_button.place(x=1039, y=777, width=157, height=47)
    print_button.place(x=1232, y=713, width=157, height=47)
    clear_button.place(x=1232, y=777, width=157, height=47)
    quick_att_btn.place(x=823, y=841, width=157, height=47)
    reset_quick_att_btn.place(x=1039, y=841, width=157, height=47)

    # Place entry widgets
    rfid_number_entry.place(x=1023, y=263, width=223, height=59)
    roll_number_entry.place(x=1023, y=364, width=386, height=59)
    from_date_entry.place(x=1043, y=490, width=157, height=30)
    to_date_entry.place(x=1232, y=490, width=157, height=30)
    month_entry.place(x=1023, y=566, width=386, height=59)
    scan_button.place(x=1252, y=263, width=157, height=59)

    rfid_number_entry.focus()


    today_data()
    clear_table()
    window.mainloop()



def quick_attendance_menu():  #######quickattendance----------------------------
    # hide the existing buttons
    global button_image_1, ltime, name_label, name_entry, search_button, roll_number_label, attendance_table, status1, status0, name
    button_1.place_forget()
    button_2.place_forget()
    button_3.place_forget()
    button_4.place_forget()
    button_5.place_forget()
    button_6.place_forget()
    button_7.place_forget()
    button_8.place_forget()
    l1.place_forget()

    my_font = ('times', 40, 'bold')

    rfid_data = []

    def on_key_press(key):
        nonlocal rfid_data
        try:
            # Check if the key is alphanumeric
            if key.keysym == "Escape":
                login()

            if key.char.isalnum():
                if len(rfid_data) == 0:
                    rfid_data = []
                    print("cleared")
                    rfid_data.clear()
                    rfid_data.clear()
                rfid_data.append(key.char)
                if len(rfid_data) == 10:
                    rf_join_data = ''.join(rfid_data)
                    current_atte(rf_join_data)
                    print("rfid", rf_join_data)
                    rfid_data.clear()
                    rfid_data.clear()
                    update_attendance_table()

        except Exception as e:
            print(e)
            # Special keys (like Ctrl, Alt, etc.) will raise an AttributeError as they do not have 'char' attribute
            # pass

    def update_attendance_table():

        cursor.execute("SELECT DISTINCT name,roll_no,rfid  FROM quick_att")
        data = cursor.fetchall()

        for row in attendance_table.get_children():
            attendance_table.delete(row)
        for record in data:
            attendance_table.insert('', 'end', text=record[0], values=record[1:4])


    today = date.today().strftime("%Y_%m_%d")
    attendance_table = ttk.Treeview(window, columns=("Name", "Time Stamp", "Roll Number", "RF Number"))
    # Create an instance of Style widget
    style = ttk.Style()
    style.theme_use('default')

    # attendance_table.column("# 0", anchor=CENTER, stretch=NO, width=150)
    # attendance_table.heading("RF Number", text="RF Number")
    attendance_table.heading("#0", text="S.no")
    attendance_table.column("# 0", anchor=CENTER, stretch=NO, width=60)
    attendance_table.heading("Name", text="Name")
    attendance_table.column("# 1", anchor=CENTER, stretch=NO, width=160)
    attendance_table.heading("Time Stamp", text="Time Stamp")
    attendance_table.column("# 2", anchor=CENTER, stretch=NO, width=140)
    attendance_table.heading("Roll Number", text="Roll Number")
    attendance_table.column("# 3", anchor=CENTER, stretch=NO, width=130)
    attendance_table.heading("RF Number", text="RF Number")
    attendance_table.column("# 4", anchor=CENTER, stretch=NO, width=130)
    attendance_table.place(x=70, y=325, width=600.0, heigh=552.0)

    def current_atte(rfid_number):
        connection = sqlite3.connect('attendance_system.db')
        cursor = connection.cursor()
        global status1, name_of_roll

        cursor.execute("SELECT roll_no FROM registered_users WHERE rfid_number = ?", (rfid_number,))
        result = cursor.fetchone()

        if result:
            cursor.execute("SELECT name FROM registered_users WHERE rfid_number = ?", (rfid_number,))
            name_of = cursor.fetchone()
            if name_of:
                name_of_roll = name_of[0].upper()
            cursor.execute("INSERT INTO quick_att (rfid, roll_no,name) VALUES (?, ?,?)", (rfid_number, result[0],name_of[0]))
            roll_number_label.config(text=f"{result[0]}\n{name_of_roll}")
            status1 = Label(window, text="PRESENT", font=my_font, borderwidth=0,
                            highlightthickness=0, bg="green", fg="white")
            status1.place(x=733.0, y=700.0, width=610.0, height=100.0)
            update_attendance_table()
            connection.commit()
        else:
            roll_number_label.config(text=f"Unknown - {rfid_number}")
            status1 = Label(window, text="UNKNOWN", font=my_font, borderwidth=0,
                            highlightthickness=0, bg="red", fg="white")
            status1.place(x=733.0, y=700.0, width=610.0, height=100.0)
        # roll_number_label.config(text="")


        connection.close()

    status1 = Label(window, text="UNKNOWN", font=my_font, borderwidth=0,
                    highlightthickness=0, bg="red", fg="white")

    ##sample----------------------
    name_label = Label(window, text="Enter Name:")
    name_entry = Entry(window)
    #search_button = Button(window, text="Search", command=current_atte)
    roll_number_label = Label(window, text="Next", font=my_font, borderwidth=0, highlightthickness=0, bg="#070c40",
                              fg="white")
    head_label = Label(window, text="Quick Attendance", font=my_font, borderwidth=0, highlightthickness=0, bg="#070c40",
                       fg="white")


    roll_number_label.place(x=733.0, y=527.0, width=610.0, height=150.0)
    head_label.place(x=420.0, y=230.0, width=610.0, height=70.0)

    # sampleee_____________
    def my_time_2():
        time_string = time.strftime('%I:%M:%S %p / %d-%m-%Y')
        ltime.config(text=time_string)
        ltime.after(1000, my_time_2)


    ltime = Button(window, font=my_font, borderwidth=0, highlightthickness=0,bg="#013f95", fg="white")
    ltime.place(x=740.0,
                y=330.0,
                width=595.0,
                height=86.0)

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

    """def on_key_press(event):
        if event.keysym == "Escape":
            login()
"""
    window.bind("<Key>", on_key_press)
    my_time_2()
    update_attendance_table()
    # listener = keyboard.Listener(on_press=on_key_press)
    # listener.start()
    window.mainloop()

def register_menu():
    global button_image_1, ltime,scan_rfid,name_entry,roll_no_entry
    # button_1.place_forget()
    button_2.place_forget()
    button_3.place_forget()
    button_4.place_forget()
    button_5.place_forget()
    button_6.place_forget()
    button_7.place_forget()
    button_8.place_forget()
    l1.place_forget()

    def scan_butn_reg():
        global scan_rfid,name_entry,roll_no_entry,hello_label
        scan_rfid.delete(0, "end")
        hello_label.destroy()
        scan_rfid.focus()


    def register_user():
        global scan_rfid,name_entry,roll_no_entry,hello_label
        try:
            rfid = scan_rfid.get()
            name = name_entry.get()
            roll_no = roll_no_entry.get()
            category = user_var.get()
            if name_entry.get().strip() != '' and roll_no_entry.get().strip() != '' and user_var.get().strip() != '':
                cursor.execute(
                    "INSERT INTO registered_users (rfid_number,name,roll_no,category) VALUES (?,?,?,?)",
                    (rfid, name, roll_no, category))
                connection.commit()
                name_upper=name.upper()
                hello_label = Label(window, text=f"REGISTERED SUCCESFULLY {name_upper}", bg="green", fg="white",
                                    font=("Arial", 20, 'bold'))
                hello_label.place(x=240, y=800, width=986, height=65)

                name_entry.delete(0, "end")
                roll_no_entry.delete(0, "end")
                scan_rfid.delete(0, "end")

                scan_rfid.focus()

            else:
                hello_label = Label(window, text="FILL ALL THE DETAILS", bg="red", fg="white",
                                    font=("Arial", 20))
                hello_label.place(x=240, y=800, width=986, height=65)
        except Exception as e:
            hello_label = Label(window, text=f"ERROR IN REGISTRATION {e}", bg="red", font=("Arial", 20))
            hello_label.place(x=240, y=800, width=986, height=65)

    name_label = Label(window, text="Name:", font=("Arial", 40, 'bold'), fg="#013f95",bg="white")
    name_entry = Entry(window, font=("Arial", 30, 'bold'), fg="black", bg='white', insertbackground='red')
    roll_no_label = Label(window, text="Roll No:", font=("Arial", 40, 'bold'), fg="#013f95",bg="white")
    roll_no_entry = Entry(window, font=("Arial", 30, 'bold'), fg="black", bg='white', insertbackground='red')
    rfid_no_label = Label(window, text="RFID No:", font=("Arial", 40, 'bold'), fg="#013f95",bg="white")
    rfid_no_entry = Label(window, font=("Arial", 30, 'bold'), fg="black", state='disabled', bg='#070c40')
    scan_button = Button(window, text="Scan", fg="#1d2f71", font=("Arial", 20, 'bold'),command=scan_butn_reg)
    submit_button = Button(window, text="Submit", fg="#1d2f71", font=("Arial", 20, 'bold'), command=register_user)
    banner_label = Label(window, text="New Registration", font=("Arial", 40, 'bold'), fg="white",bg="#070c40")
    category_label = Label(window, text="Category / Year", font=("Arial", 30, 'bold'), fg="#013f95",bg="white")
    user_var = StringVar(window)
    user_var.set("")  # Default selection
    user_dropdown = OptionMenu(window, user_var, "1st", "2nd", "3rd", "4th", "PIC", "INTERN","FACULTY", "GUEST", "SHORT-TERM")
    user_dropdown.config(font=("Arial", 20, 'bold'), fg="white", bg="#070c40")
    user_dropdown.place(x=642, y=640, width=226.0, height=59.0)
    scan_rfid = Entry(window, font=my_font, borderwidth=0, highlightthickness=0,
                      bg="#013f95", fg="white")
    scan_rfid.place(x=642, y=340, width=328, height=66)
    scan_rfid.focus_set()


    name_label.place(x=250, y=440, width=300, height=66)
    name_entry.place(x=642, y=440, width=596, height=66)
    roll_no_label.place(x=250, y=540, width=300, height=66)
    roll_no_entry.place(x=642, y=540, width=596, height=66)
    rfid_no_label.place(x=250, y=340, width=300, height=66)
    rfid_no_entry.place(x=642, y=340, width=328, height=66)
    scan_button.place(x=1020, y=340, width=218, height=66)
    category_label.place(x=250, y=640, width=300, height=66)
    submit_button.place(x=642, y=730, width=348, height=58)


    # Start the thread
    banner_label.place(x=240, y=230, width=986, height=70)

    def on_key_press(event):
        if event.keysym == "Escape":
            home()

    window.bind("<Key>", on_key_press)
    window.mainloop()

def rfid_status():
    button_1.place_forget()
    button_2.place_forget()
    button_3.place_forget()
    button_4.place_forget()
    button_5.place_forget()
    button_6.place_forget()
    button_7.place_forget()
    button_8.place_forget()
    l1.place_forget()

    def show_message():
        # Message to be displayed
        message = ('''registered_users : 

        Name    |    roll_no   |   rfid_number    |    category


        att_2024_04_20 : 

        rfid    |    timestamp(yyyy-mm-dd hh:mm:ss)    |    roll_no


        quick_att: 

        Rfid    |    timestamp(yyyy-mm-dd hh:mm:ss)      |    roll_no


        cred:

        Username    |    password


        (Note : Do not include the column names in the csv , it will be added to the db )

''')

        # Create a message box with the given message
        messagebox.showinfo("DESCRIBE TABLE", message)

    def upload_csv_to_db():
        # Get the selected database file
        database_file = selector_db1_var.get()

        # Get the selected CSV file
        csv_file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        try:  # Read the CSV file
            with open(csv_file, 'r') as f:
                reader = csv.reader(f)
                header = next(reader)
                # Insert the CSV data into the table
                for row in reader:
                    values = ", ".join(["?" for col in row])
                    cursor.execute(f"INSERT INTO {database_file} VALUES ({values});", row)
            import_status = Label(window, text="IMPORT SUCCESSFULL", bg="green", fg="white", font=("Arial", 20, 'bold'))
            import_status.place(x=62, y=500, height=85, width=728)
        except Exception as e:
            import_status = Label(window, text=f"IMPORT FAILED -- {e}", bg="red", fg="white",
                                  font=("Arial", 20, 'bold'))
            import_status.place(x=62, y=500, height=85, width=728)

    def execute_query():
        # global cus_query_status
        connection = sqlite3.connect('attendance_system.db')
        cursor = connection.cursor()

        try:
            query = query_add.get("1.0", END)
            cred_words = ["cred", "password"]
            if any(word in query.lower() for word in cred_words):
                cus_query_status = Label(window, text="Access Denied <confidential>", font=("Arial", 20, 'bold'),
                                         bg="red",
                                         fg='blue')
                cus_query_status.place(x=863, y=174, height=96, width=500)
            else:
                cursor.execute(query)  # Execute the query
                results = cursor.fetchall()  # Get the results
                output_query.delete(1.0, END)  # Clear the output_query text box
                for row in results:
                    output_query.insert(END, str(row) + "\n")  # Show the results in the output_query text box
                connection.close()
                cus_query_status = Label(window, text="Query Executed", font=("Arial", 20, 'bold'), bg="green",
                                         fg='white')
                cus_query_status.place(x=863, y=174, height=96, width=500)
                connection.close()
        except Exception as e:
            output_query.delete(1.0, END)
            output_query.insert(END, f"Error -- {e}")
            output_query.tag_config("red", foreground="red")
            output_query.tag_add("red", 1.0, "2.0")
            cus_query_status = Label(window, text="Error in Query", font=("Arial", 20, 'bold'), bg="red", fg='white')
            cus_query_status.place(x=863, y=174, height=96, width=500)

    def status():
        try:
            cursor.execute("SELECT * FROM att_2024_04_20")
            db_status_data.config(text="Running", font=("Arial", 20, 'bold'), bg="green", fg='white')
        except Exception as e:
            if "database is locked" == str(e):
                db_status_data.config(text="Error: The database is locked", font=("Arial", 14, 'bold'), bg="red",
                                      fg='white')
            elif "Cannot operate on a closed database." in str(e):
                db_status_data.config(text="Error: The database is closed", font=("Arial", 14, 'bold'), bg="red",
                                      fg='white')
            else:
                db_status_data.config(text=f"Error: {e} ", font=("Arial", 12, 'bold'), bg="red", fg='white')

    def export_to_csv():
        # global column_names
        downloads_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        csv_filename = os.path.join(downloads_dir, f"output_data{timestamp}.csv")

        query = query_add.get("1.0", END)

        try:
            # Execute the query
            cursor.execute(query)

            # Fetch all rows from the executed query
            rows = cursor.fetchall()

            # Get column names from the cursor description
            column_names = [description[0] for description in cursor.description]

            # Open the CSV file for writing
            with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                # Write the column headers to the CSV file
                writer.writerow(column_names)
                # Write all rows to the CSV file
                writer.writerows(rows)

            cus_query_status = Label(window, text=f"Data exported successfully to \n {csv_filename}", bg="green",
                                     fg="white", font=("Arial", 13, 'bold'))
            cus_query_status.place(x=863, y=174, height=96, width=500)

        except Exception as e:
            if query == "":
                cus_query_status = Label(window, text=f"Enter the query -- {e}", bg="red", fg="white",
                                         font=("Arial", 20, 'bold'))
                cus_query_status.place(x=863, y=174, height=96, width=500)
            else:
                cus_query_status = Label(window, text=f"Error downloading csv -- {e}", bg="red", fg="white",
                                         font=("Arial", 14, 'bold'))
                cus_query_status.place(x=863, y=174, height=96, width=500)

    def clear_text():
        output_query.delete(1.0, END)
        query_add.delete(1.0, END)
        cus_query_status = Label(window, text="-- Execute Query --", font=("Arial", 20, 'bold'), bg="#B3C6FF",
                                 fg='black')
        cus_query_status.place(x=863, y=174, height=96, width=500)

    # Create Labels
    status_head = Label(window, text="STATUS", bg="#070c40", fg="white", font=("Arial", 32, 'bold'))
    cus_query_head = Label(window, text="CUSTOM QUERY EDITOR", bg="#070c40", fg="white", font=("Arial", 32, 'bold'))
    import_status = Label(window, text="-- Import Data --", font=("Arial", 20, 'bold'), bg="#B3C6FF", fg='black')
    import_head = Label(window, text="DATA IMPORTER", bg="#070c40", fg="white", font=("Arial", 32, 'bold'))
    cus_query_status = Label(window, text="-- Execute Query --", font=("Arial", 20, 'bold'), bg="#B3C6FF", fg='black')
    select_db1 = Label(window, text="SELECT DATABASE", font=("Arial", 20, 'bold'), bg="#013f95", fg='white')
    select_db2 = Label(window, text="SELECT DATABASE", font=("Arial", 20, 'bold'), bg="#013f95", fg='white')
    reader_status = Label(window, text="Reader status", font=("Arial", 25, 'bold'), bg="#013f95", fg='white')
    reader_status_data = Label(window, text="reader_status_data")
    db_status = Label(window, text="DB Status", font=("Arial", 25, 'bold'), bg="#013f95", fg='white')
    db_status_data = Label(window, text="db_status_data")
    overall_status = Label(window, text="Overall Status", font=("Arial", 25, 'bold'), bg="#013f95", fg='white')
    overall_status_data = Label(window, text="overall_status_data")

    # Create OptionMenu for dropdowns
    selector_db1_var = StringVar(window)
    selector_db2_var = StringVar(window)

    selector_db1_var.set("Select db")
    selector_db2_var.set("Select db")

    selector_db1 = OptionMenu(window, selector_db1_var, "registered_users", "quick_att", "att_2024_04_20",
                              "registered_users")
    selector_db2 = OptionMenu(window, selector_db2_var, "registered_users", "quick_att", "att_2024_04_20",
                              "registered_users")
    selector_db1.config(font=("Arial", 20, 'bold'), fg="#013f95", bg="white")
    selector_db2.config(font=("Arial", 20, 'bold'), fg="#013f95", bg="white")
    # Create Buttons
    refresh = Button(window, text="Refresh", command=lambda: rfid_status(), font=("Arial", 20, 'bold'), bg="white",
                     fg='#013f95')

    import_btn = Button(window, text="IMPORT DATA", command=upload_csv_to_db, font=("Arial", 20, 'bold'), bg="white",
                        fg='#013f95')
    table_info_btn = Button(window, text="TABLE INFOS", command=show_message, font=("Arial", 20, 'bold'), bg="white",
                            fg='#013f95')
    dwn_csv_btn = Button(window, text="DOWNL CSV", command=export_to_csv, font=("Arial", 20, 'bold'), bg="white",
                         fg='#013f95')
    executer_btn = Button(window, text="EXECUTE", command=execute_query, font=("Arial", 20, 'bold'), bg="white",
                          fg='#013f95')
    clear_btn = Button(window, text="CLEAR", command=lambda: clear_text(), font=("Arial", 20, 'bold'), bg="white",
                       fg='#013f95')

    # Create Text Boxes
    query_add = Text(window, height=126, width=500, font=("Arial", 14, 'bold'))
    output_query = Text(window, height=126, width=500, font=("Arial", 14))

    # Place Labels
    status_head.place(x=68, y=47, height=77, width=772)
    cus_query_head.place(x=863, y=96, height=65, width=500)
    import_status.place(x=62, y=500, height=85, width=728)
    import_head.place(x=62, y=406, height=66, width=728)
    cus_query_status.place(x=863, y=174, height=96, width=500)
    select_db1.place(x=863, y=295, height=59, width=225)
    select_db2.place(x=62, y=603, height=59, width=225)

    reader_status.place(x=68, y=149, height=47, width=213)
    reader_status_data.place(x=311, y=149, height=47, width=213)
    db_status.place(x=68, y=222, height=47, width=213)
    db_status_data.place(x=311, y=222, height=47, width=213)
    overall_status.place(x=68, y=295, height=47, width=213)
    overall_status_data.place(x=311, y=295, height=47, width=213)

    # Place OptionMenu
    selector_db1.place(x=1103, y=295, height=59, width=259)
    selector_db2.place(x=311, y=603, height=59, width=480)

    # Place Buttons
    refresh.place(x=547, y=174, height=134, width=243)

    import_btn.place(x=218, y=705, height=54, width=355)
    table_info_btn.place(x=218, y=784, height=54, width=355)
    dwn_csv_btn.place(x=863, y=705, height=54, width=243)
    executer_btn.place(x=1113, y=705, height=54, width=243)
    clear_btn.place(x=986, y=787, height=54, width=243)

    # Place Text Boxes
    query_add.place(x=863, y=389, height=126, width=500)
    output_query.place(x=863, y=543, height=126, width=500)

    status()


def home():
    global l1, button_1, button_2, button_3, button_4, button_5, button_6, button_7, button_8,thread
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
    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: window.destroy(),
        relief="flat"
    )
    button_1.place(
        x=142.0,
        y=46.0,
        width=1136.0,
        height=166.0
    )
    # time
    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
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
        command=lambda: quick_attendance_menu(),
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
        command=lambda: rfid_status(),
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
        command=lambda:view_panel(),
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
        #x=1250,
        y=363.0,
        width=383.0,
        height=105.0
    )


    l1 = Button(window, font=my_font, borderwidth=0,
                    highlightthickness=0, bg="#013f95", fg="white")
    l1.place(x=412.0,
             y=244.0,
             width=595.0,
             height=86.0)
    my_time()

    def on_key_press(event):
        if event.keysym == "Escape":
            home()
        if event.char.lower() == "a":
            attendance_menu()
    window.bind("<Key>", on_key_press)
    window.mainloop()

#window.bind("<Key>", on_key_press)
window.resizable(True, True)


home()
