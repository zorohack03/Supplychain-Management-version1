import tkinter as tk
from tkinter import messagebox 
import mysql.connector

class Material:
    def __init__(self, name, unit_price):
        self.name = name
        self.unit_price = unit_price

    def __str__(self):
        return f"{self.name} - Price: ${self.unit_price}"

class Producer:
    def __init__(self, name, productA_quantity, productB_quantity):
        self.name = name
        self.productA_quantity = productA_quantity
        self.productB_quantity = productB_quantity

    def __str__(self):
        return f"{self.name} produces: ProductA Quantity on hand: {self.productA_quantity}, ProductB Quantity on hand: {self.productB_quantity}"

class RawMaterial(Material):
    def __init__(self, name, unit_price):
        super().__init__(name, unit_price)

class Warehouse:
    def __init__(self, name, raw_material, quantity_need, warehouse_id):
        self.name = name
        self.raw_material = RawMaterial(raw_material, 0)
        self.quantity_need = quantity_need
        self.warehouse_id = warehouse_id

    def __str__(self):
        return f"{self.name} Orders: for {self.quantity_need} units of {self.raw_material.name}"

class DeliverOrder:
    def __init__(self, warehouse, producer, quantity):
        self.warehouse = warehouse
        self.producer = producer
        self.quantity = quantity

    def __str__(self):
        return f"Deliver Order from {self.warehouse.name} to {self.producer.name} for {self.quantity} units of {self.warehouse.raw_material.name}"

class DeliverOrderManager:
    def __init__(self, db_cursor, db_connection):
        self.deliver_orders = []
        self.db_cursor = db_cursor
        self.db_connection = db_connection
        self.stock_requests = []

    def add_request(self, request_text):
        self.stock_requests.append(request_text)

    def create_deliver_order(self, warehouse, producer, quantity):
        product_name = warehouse.raw_material.name

        if product_name == "ProductA":
            if producer.productA_quantity >= warehouse.quantity_need:
                deliver_order = DeliverOrder(warehouse, producer, quantity)
                self.deliver_orders.append(deliver_order)
                producer.productA_quantity -= quantity
                warehouse.quantity_need -= quantity
                self.update_producer_product_quantity(producer, 'productA_quantity', producer.productA_quantity)
                self.update_warehouse_product_quantity(warehouse.warehouse_id, product_name, quantity)
                return deliver_order
            else:
                return "Not enough ProductA on the producer's hand."
        elif product_name == "ProductB":
            if producer.productB_quantity >= warehouse.quantity_need:
                deliver_order = DeliverOrder(warehouse, producer, quantity)
                self.deliver_orders.append(deliver_order)
                producer.productB_quantity -= quantity
                warehouse.quantity_need -= quantity
                self.update_producer_product_quantity(producer, 'productB_quantity', producer.productB_quantity)
                self.update_warehouse_product_quantity(warehouse.warehouse_id, product_name, quantity)
                return deliver_order
            else:
                return "Not enough ProductB on the producer's hand."
        else:
            return "Invalid product name."

    def update_producer_product_quantity(self, producer, column_name, new_quantity):
        if self.db_cursor and self.db_connection:
            self.db_cursor.execute(
                f"UPDATE producer SET {column_name} = %s WHERE name = %s",
                (new_quantity, producer.name)
            )
            self.db_connection.commit()

    def update_warehouse_product_quantity(self, warehouse_id, product_name, change):
        if self.db_cursor and self.db_connection:
            self.db_cursor.execute(
                "UPDATE warehouse SET quantity = quantity + %s WHERE id = %s AND product_name = %s",
                (change, warehouse_id, product_name)
            )
            self.db_connection.commit()

    def list_deliver_orders(self):
        for deliver_order in self.deliver_orders:
            print(deliver_order)

    def list_stock_requests(self):
        return "\n".join(self.stock_requests)

class DeliverOrderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Factory Management")

        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="supply_chain_management"
        )
        self.db_cursor = self.db_connection.cursor()

        self.create_producers()
        self.create_warehouses()
        self.create_deliver_order_manager()
        self.create_gui_elements()

    def create_producers(self):
        self.db_cursor.execute("SELECT * FROM producer WHERE name='Producers'")
        producer_data = self.db_cursor.fetchone()
        self.producers = Producer("Producers", producer_data[2], producer_data[3])

    def create_warehouses(self):
        # Fetch warehouse data from database or initialize them with proper ids
        # Assuming the warehouses have unique ids in your database
        self.warehouse1 = Warehouse("Warehouse1", "ProductA", 50, warehouse_id=1)
        self.warehouse2 = Warehouse("Warehouse2", "ProductB", 100, warehouse_id=2)

    def create_deliver_order_manager(self):
        self.manager = DeliverOrderManager(self.db_cursor, self.db_connection)

    def create_gui_elements(self):
        self.create_producers_frame()
        self.create_warehouses_frame()
        self.create_deliver_order_frame()
        self.create_stock_request_frame()

    def create_producers_frame(self):
        self.producers_frame = tk.Frame(self.root)
        self.producers_frame.pack()
        producers_label = tk.Label(self.producers_frame, text="Producers")
        producers_label.pack()

        self.producers_info_label = tk.Label(self.producers_frame, text=str(self.producers))
        self.producers_info_label.pack()

    def create_warehouses_frame(self):
        self.warehouses_frame = tk.Frame(self.root)
        self.warehouses_frame.pack()
        warehouses_label = tk.Label(self.warehouses_frame, text="Orders")
        warehouses_label.pack()

        self.warehouse1_label = tk.Label(self.warehouses_frame, text=str(self.warehouse1))
        self.warehouse1_label.pack()
        self.warehouse2_label = tk.Label(self.warehouses_frame, text=str(self.warehouse2))
        self.warehouse2_label.pack()

    def create_deliver_order_frame(self):
        deliver_order_frame = tk.Frame(self.root)
        deliver_order_frame.pack()
        create_order_label = tk.Label(deliver_order_frame, text="Create Deliver Order")
        create_order_label.pack()

        warehouse_label = tk.Label(deliver_order_frame, text="Enter the warehouse name (1/2):")
        warehouse_label.pack()
        self.warehouse_entry = tk.Entry(deliver_order_frame)
        self.warehouse_entry.pack()

        quantity_label = tk.Label(deliver_order_frame, text="Enter the quantity:")
        quantity_label.pack()
        self.quantity_entry = tk.Entry(deliver_order_frame)
        self.quantity_entry.pack()

        create_button = tk.Button(deliver_order_frame, text="Create Order", command=self.create_deliver_order)
        create_button.pack()

    def create_stock_request_frame(self):
        stock_request_frame = tk.Frame(self.root)
        stock_request_frame.pack()
        stock_request_label = tk.Label(stock_request_frame, text="Stock Requests")
        stock_request_label.pack()

        self.stock_request_list = tk.Label(stock_request_frame, text="")
        self.stock_request_list.pack()

        self.update_stock_requests()

    def create_deliver_order(self):
        warehouse_name = self.warehouse_entry.get()
        quantity = self.quantity_entry.get()

        try:
            warehouse_name = int(warehouse_name)
            quantity = int(quantity)
        except ValueError:
            tk.messagebox.showerror("Error", "Invalid input. Please enter numeric values.")
            return

        if warehouse_name == 1:
            warehouse = self.warehouse1
        elif warehouse_name == 2:
            warehouse = self.warehouse2
        else:
            tk.messagebox.showerror("Error", "Invalid warehouse name. Please enter 1 or 2.")
            return

        result = self.manager.create_deliver_order(warehouse, self.producers, quantity)
        if isinstance(result, DeliverOrder):
            tk.messagebox.showinfo("Success", f"Deliver order created: {result}")
            self.update_gui_elements()
        else:
            tk.messagebox.showerror("Error", result)

    def update_gui_elements(self):
        self.create_producers()
        self.producers_info_label.config(text=str(self.producers))

        self.warehouse1_label.config(text=str(self.warehouse1))
        self.warehouse2_label.config(text=str(self.warehouse2))
        self.update_stock_requests()

    def update_stock_requests(self):
        stock_requests = self.manager.list_stock_requests()
        self.stock_request_list.config(text=stock_requests)

def main():
    root = tk.Tk()
    app = DeliverOrderApp(root)
    root.state('zoomed')
    root.mainloop()

if __name__ == "__main__":
    main()
