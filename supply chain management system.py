import tkinter as tk
import os
import bcrypt
import mysql.connector

def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password

def verify_login(option, username, password):
    if option == "Labors":
        os.system("python labour.py")
        return

    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='MySQL@04',
        database='supply_chain_management'
    )
    cursor = conn.cursor()

    query = "SELECT password FROM user_credentials WHERE username = %s"
    cursor.execute(query, (username,))
    stored_password = cursor.fetchone()

    if stored_password:
        hashed_password = stored_password[0].encode('utf8')

        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            print(f"Login Successful! Logging in as {option} with Username: {username}")
            open_production_file(option)
        else:
            print("Invalid username or password")
    else:
        print("Invalid username or password")

    conn.close()

def register_new_user(option, username, password):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='MySQL@04',
        database='supply_chain_management'
    )
    cursor = conn.cursor()

    hashed_password = hash_password(password)
    query = "INSERT INTO user_credentials (username, password) VALUES (%s, %s)"
    cursor.execute(query, (username, hashed_password))
    conn.commit()

    print(f"Registration successful for {option} with Username: {username}")
    conn.close()

def open_production_file(role):
    role_file = None

    if role == "Purchase Production Manager":
        role_file = "purchasemanager.py"
    elif role == "Delivery Production Manager":
        role_file = "deliverymanager.py"
    elif role == "Warehouse Manager":
        role_file = "warehouse.py"
    elif role == "Labors":
        role_file = "labour.py"

    if role_file and os.path.exists(role_file):
        os.system(f"python {role_file}")
    else:
        print(f"File {role_file} does not exist.")

def select_option(option):
    global username_entry, password_entry
    if option == "Labors":
        os.system("python labour.py")
        return

    def back_to_options():
        for widget in root.winfo_children():
            widget.destroy()
        main_window()

    def login():
        username = username_entry.get()
        password = password_entry.get()
        verify_login(option, username, password)

    def signup():
        username = username_entry.get()
        password = password_entry.get()
        register_new_user(option, username, password)

    for widget in root.winfo_children():
        widget.destroy()

    title_label = tk.Label(root, text=option, font=("Helvetica", 30))
    title_label.pack()

    entry_frame = tk.Frame(root)
    entry_frame.pack()

    username_label = tk.Label(entry_frame, text="Username:")
    username_label.grid(row=0, column=0, padx=10, pady=10)

    username_entry = tk.Entry(entry_frame, width=30)
    username_entry.grid(row=0, column=1, padx=10, pady=10)

    password_label = tk.Label(entry_frame, text="Password:")
    password_label.grid(row=1, column=0, padx=10, pady=10)

    password_entry = tk.Entry(entry_frame, show="*", width=30)
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    login_button = tk.Button(root, text="Login", command=login)
    login_button.pack()

    signup_button = tk.Button(root, text="Signup", command=signup)
    signup_button.pack()

    back_button = tk.Button(root, text="Back", command=back_to_options)
    back_button.pack()

def main_window():
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Supply Chain Management System")

    title_label = tk.Label(root, text="Supply Chain Management System", font=("Helvetica", 24))
    title_label.pack()

    options_frame = tk.Frame(root)
    options_frame.pack()

    options = ["Purchase Production Manager", "Delivery Production Manager", "Warehouse Manager", "Labors"]
    for option in options:
        button = tk.Button(options_frame, text=option, width=30, height=5, command=lambda opt=option: select_option(opt))
        button.pack(side="left", padx=20, pady=20)

root = tk.Tk()
root.state('zoomed')
main_window()
footer_label = tk.Label(root, text="@supply_chain_management_team", font=("Helvetica", 10))
footer_label.pack(side="bottom", pady=10)
root.mainloop()
