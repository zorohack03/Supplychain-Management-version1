import tkinter as tk
import mysql.connector

class Material:
    def __init__(self, name, unit_price):
        self.name = name
        self.unit_price = unit_price

    def __str__(self):
        return f"{self.name} - Price: ${self.unit_price}"

class Supplier:
    def __init__(self, name, steel_quantity_on_supplier, plastic_quantity_on_supplier, amount_steel, amount_plastic):
        self.name = name
        self.steel_quantity_on_supplier = steel_quantity_on_supplier
        self.plastic_quantity_on_supplier = plastic_quantity_on_supplier
        self.amount_steel = amount_steel
        self.amount_plastic = amount_plastic

    def __str__(self):
        return f"{self.name} supplies: Steel Quantity on hand: {self.steel_quantity_on_supplier}, Plastic Quantity on hand: {self.plastic_quantity_on_supplier}. {self.name} price for steel is {self.amount_steel}--{self.name} price for plastic is {self.amount_plastic}"

class RawMaterial(Material):
    def __init__(self, name, unit_price):
        super().__init__(name, unit_price)

class Factory:
    def __init__(self, name, raw_material, quantity_need):
        self.name = name
        self.raw_material = RawMaterial(raw_material, 0)
        self.quantity_need = quantity_need

    def __str__(self):
        return f"{self.name} Orders: for {self.quantity_need} units of {self.raw_material.name}"

class PurchaseOrder(Material):
    def __init__(self, factory, supplier, quantity):
        super().__init__(factory.raw_material.name, 0)
        self.factory = factory
        self.supplier = supplier
        self.quantity = quantity
        if self.name.lower() == "steel":
            self.total_cost = quantity * supplier.amount_steel
        else:
            self.total_cost = quantity * supplier.amount_plastic

    def __str__(self):
        return f"Purchase Order from {self.factory.name} to {self.supplier.name} for {self.quantity} units of {self.name}. The cost is {self.total_cost}"

class PurchaseOrderManager:
    def __init__(self):
        self.purchase_orders = []
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="supply_chain_management"
        )
        self.db_cursor = self.db_connection.cursor()

    def get_factory_raw_material(self, factory_name):
        query = "SELECT raw_material FROM factories WHERE name = %s"
        self.db_cursor.execute(query, (factory_name,))
        result = self.db_cursor.fetchone()
        if result:
            return result[0].lower()  # Ensure raw material is in lower case for comparison
        else:
            return None

    def create_purchase_order(self, factory, supplier, quantity):
        if factory.raw_material.name == "steel":
            if supplier.steel_quantity_on_supplier >= factory.quantity_need:
                purchase_order = PurchaseOrder(factory, supplier, quantity)
                self.purchase_orders.append(purchase_order)
                supplier.steel_quantity_on_supplier -= quantity
                factory.quantity_need -= quantity
                self.update_producer_quantities("steel", quantity)
                return purchase_order
            else:
                print("Not enough steel on the supplier's hand.")
        elif factory.raw_material.name == "plastic":
            if supplier.plastic_quantity_on_supplier >= factory.quantity_need:
                purchase_order = PurchaseOrder(factory, supplier, quantity)
                self.purchase_orders.append(purchase_order)
                supplier.plastic_quantity_on_supplier -= quantity
                factory.quantity_need -= quantity
                self.update_producer_quantities("plastic", quantity)
                return purchase_order
            else:
                print("Not enough plastic on the supplier's hand.")
        else:
            print("Invalid raw material name.")

    def update_producer_quantities(self, raw_material, quantity):
        if raw_material == "steel":
            productA_quantity = quantity * 10
            update_query = """
            UPDATE producer
            SET productA_quantity = productA_quantity + %s
            WHERE name = 'Producers'
            """
            self.db_cursor.execute(update_query, (productA_quantity,))
        elif raw_material == "plastic":
            productB_quantity = quantity * 15
            update_query = """
            UPDATE producer
            SET productB_quantity = productB_quantity + %s
            WHERE name = 'Producers'
            """
            self.db_cursor.execute(update_query, (productB_quantity,))
        self.db_connection.commit()

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Supply Chain Management System")

        self.purchase_order_manager = PurchaseOrderManager()

        self.create_widgets()

    def create_widgets(self):
        
        def submit_purchase_order():
            factory_name = factory_name_entry.get()
            supplier_name = supplier_name_entry.get()
            quantity = int(quantity_entry.get())

            raw_material = self.purchase_order_manager.get_factory_raw_material(factory_name)
            if raw_material is None:
                purchase_order_text.insert(tk.END, f"Invalid factory name: {factory_name}\n")
                return

            factory = Factory(factory_name, raw_material, quantity)  
            supplier = Supplier(supplier_name, 100, 100, 20, 30)  

            created_order = self.purchase_order_manager.create_purchase_order(factory, supplier, quantity)
            if created_order:
                purchase_order_text.insert(tk.END, f"Purchase order created: {created_order}\n")

      
        factory_name_label = tk.Label(self, text="Enter the factory name (Factory1/Factory2):")
        factory_name_label.pack()

        factory_name_entry = tk.Entry(self)
        factory_name_entry.pack()

        supplier_name_label = tk.Label(self, text="Enter the supplier name (Supplier 1/Supplier 2):")
        supplier_name_label.pack()

        supplier_name_entry = tk.Entry(self)
        supplier_name_entry.pack()

        quantity_label = tk.Label(self, text="Enter the quantity:")
        quantity_label.pack()

        quantity_entry = tk.Entry(self)
        quantity_entry.pack()

        submit_button = tk.Button(self, text="Submit", command=submit_purchase_order)
        submit_button.pack()

        self.purchase_order_label = tk.Label(self, text="Purchase Orders:")
        self.purchase_order_label.pack()

        purchase_order_text = tk.Text(self, height=10, width=50)
        purchase_order_text.pack()

def main():
    app = Application()
    app.state('zoomed')
    app.mainloop()

if __name__ == "__main__":
    main()
