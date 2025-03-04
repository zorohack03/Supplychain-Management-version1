import tkinter as tk
import mysql.connector
import tkinter.messagebox as messagebox

class LabourManagementApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Labour Management Login")
        self.root.state('zoomed')

        self.create_login_ui()

    def create_login_ui(self):
        title_label = tk.Label(self.root, text="Labour Management Login", font=("Helvetica", 24))
        title_label.pack(pady=20)

        login_frame = tk.Frame(self.root)
        login_frame.pack(pady=10)
        
        username_label = tk.Label(login_frame, text="Username:")
        username_label.grid(row=0, column=0, padx=10, pady=10)
        self.username_entry = tk.Entry(login_frame, width=30)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        password_label = tk.Label(login_frame, text="Password:")
        password_label.grid(row=1, column=0, padx=10, pady=10)
        self.password_entry = tk.Entry(login_frame, show="*", width=30)
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        login_button = tk.Button(login_frame, text="Login", command=self.verify_login)
        login_button.grid(row=2, column=0, columnspan=2, pady=10)

    def verify_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='supply_chain_management'
            )
            cursor = conn.cursor()
            query = "SELECT password FROM employees WHERE name = %s"
            cursor.execute(query, (username,))
            stored_password = cursor.fetchone()
            if stored_password:
                if password == stored_password[0]:
                    self.show_employee_details(username)
                else:
                    messagebox.showerror("Login Failed", "Invalid username or password")
            else:
                messagebox.showerror("Login Failed", "Invalid username or password")
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def show_employee_details(self, username):
        for widget in self.root.winfo_children():
            widget.destroy()
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='supply_chain_management'
        )
        cursor = conn.cursor()
        query = "SELECT name, pending_work, completed_work FROM employees WHERE name = %s"
        cursor.execute(query, (username,))
        employee_data = cursor.fetchone()

        conn.close()

        if employee_data:
            title_label = tk.Label(self.root, text="Employee Details", font=("Helvetica", 24))
            title_label.pack(pady=20)
            
            details_frame = tk.Frame(self.root)
            details_frame.pack(pady=10)

            name_label = tk.Label(details_frame, text=f"Name: {employee_data[0]}", font=("Helvetica", 16))
            name_label.pack()
            
            pending_label = tk.Label(details_frame, text=f"Pending Work: {employee_data[1]}")
            pending_label.pack()

            completed_label = tk.Label(details_frame, text=f"Completed Work: {employee_data[2]}")
            completed_label.pack()
            
            salary_status = "Salary Credited" if employee_data[1] == 0 else "Salary Not Credited"
            status_label = tk.Label(details_frame, text=f"Salary Status: {salary_status}")
            status_label.pack()

    def run(self):
        self.root.mainloop()

def main():
    app = LabourManagementApp()
    app.run()

if __name__ == "__main__":
    main()
