import tkinter as tk
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="supply_chain_management"
)
mycursor = mydb.cursor()

def display_employee_data():
    username = entry_username.get()
    password = entry_password.get()

    mycursor.execute("SELECT name, pending_work, completed_work FROM employees WHERE name = %s AND password = %s",
                     (username, password))
    data = mycursor.fetchone()

    if data:
        label_name.config(text=f"Name: {data[0]}")
        entry_pending.delete(0, tk.END)
        entry_pending.insert(tk.END, data[1]) 
        entry_completed.delete(0, tk.END)
        entry_completed.insert(tk.END, data[2])  

        
        if data[1] == 0:
            label_salary_status.config(text="Salary Credited")
        else:
            label_salary_status.config(text="Salary Not Credited")
    else:
        label_name.config(text="Employee data not found")

root = tk.Tk()
root.title("Employee Salary Tracker")

label_username = tk.Label(root, text="Username:")
label_username.pack()
entry_username = tk.Entry(root)
entry_username.pack()

label_password = tk.Label(root, text="Password:")
label_password.pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()

button = tk.Button(root, text="Login", command=display_employee_data)
button.pack()

label_name = tk.Label(root, text="Name:")
label_name.pack()

label_pending = tk.Label(root, text="Pending Work:")
label_pending.pack()
entry_pending = tk.Entry(root)
entry_pending.pack()

label_completed = tk.Label(root, text="Completed Work:")
label_completed.pack()
entry_completed = tk.Entry(root)
entry_completed.pack()

label_salary_status = tk.Label(root, text="")
label_salary_status.pack()

root.state('zoomed')
root.mainloop()



