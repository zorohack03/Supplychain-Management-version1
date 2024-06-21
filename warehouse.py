import mysql.connector
import tkinter as tk
from deliverymanager import DeliverOrderManager, DeliverOrderApp  # Add this line to import DeliverOrderManager

class Warehouse:
    def __init__(self, id, location, order_manager):
        self.id = id
        self.location = location
        self.order_manager = order_manager  # Reference to DeliverOrderManager

        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='supply_chain_management'
        )
        self.cursor = self.conn.cursor()

    def display_stock(self):
        try:
            display_query = "SELECT id, product_id, product_name, price, quantity FROM warehouse"
            self.cursor.execute(display_query)
            stock = self.cursor.fetchall()

            if not stock:
                return "No stock data found."

            display_text = "Stock:\n"
            for product in stock:
                display_text += f"Warehouse ID: {product[0]}, Product ID: {product[1]}, Product Name: {product[2]}, Price: {product[3]}, Quantity: {product[4]}\n"
            
            return display_text

        except mysql.connector.Error as err:
            return f"Error: {err}"

    def subtract_stock(self, warehouse_id, product_id, quantity):
        try:
            subtract_stock_query = "UPDATE warehouse SET quantity = quantity - %s WHERE id = %s AND product_id = %s AND quantity >= %s"
            self.cursor.execute(subtract_stock_query, (quantity, warehouse_id, product_id, quantity))
            if self.cursor.rowcount > 0:
                self.conn.commit()
                return f"Subtracted {quantity} units from Warehouse {warehouse_id}."
            else:
                return f"Insufficient stock in Warehouse {warehouse_id}."
        except mysql.connector.Error as err:
            return f"Error: {err}"

    def request_stock(self, warehouse_id, product_id, quantity):
        try:
            request_text = f"Stock request from Warehouse {warehouse_id} for Product {product_id}, Quantity {quantity}"
            self.order_manager.add_request(request_text)  # Call method to add request to DeliverOrderManager
            return f"Stock request added for Warehouse {warehouse_id}."
        except Exception as err:
            return f"Error: {err}"

    def close_db(self):
        self.conn.close()

def display_stock():
    stock_text = warehouses[0].display_stock()
    lbl_result['text'] = stock_text

def subtract_stock():
    warehouse_id = int(entry_warehouse_id.get())
    product_id = int(entry_product_id.get())
    quantity = int(entry_quantity.get())

    result = warehouses[0].subtract_stock(warehouse_id, product_id, quantity)
    lbl_result['text'] = result

def request_stock():
    warehouse_id = int(entry_warehouse_id.get())
    product_id = int(entry_product_id.get())
    quantity = int(entry_quantity.get())

    result = warehouses[0].request_stock(warehouse_id, product_id, quantity)
    lbl_result['text'] = result


root = tk.Tk()
deliver_app = DeliverOrderApp(root)
order_manager = deliver_app.manager  # Use the manager from DeliverOrderApp
warehouses = [Warehouse(1, "Warehouse 1", order_manager)]

root = tk.Tk()
root.title("Warehouse Management System")
# Widgets
lbl_warehouse_id = tk.Label(root, text="Warehouse ID:")
lbl_warehouse_id.pack()
entry_warehouse_id = tk.Entry(root)
entry_warehouse_id.pack()
lbl_product_id = tk.Label(root, text="Product ID:")
lbl_product_id.pack()
entry_product_id = tk.Entry(root)
entry_product_id.pack()
lbl_quantity = tk.Label(root, text="Quantity:")
lbl_quantity.pack()
entry_quantity = tk.Entry(root)
entry_quantity.pack()
lbl_result = tk.Label(root, text="")
lbl_result.pack()
btn_display_stock = tk.Button(root, text="Display Stock", command=display_stock)
btn_display_stock.pack()
btn_subtract = tk.Button(root, text="Subtract Stock", command=subtract_stock)
btn_subtract.pack()
btn_request = tk.Button(root, text="Request Stock", command=request_stock)
btn_request.pack()
root.state('zoomed')
root.mainloop()
