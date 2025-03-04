# Supply Chain Management System

![Supply Chain Management](https://img.freepik.com/free-vector/diagram-supply-chain-management_1308-100127.jpg)

## Overview

The Supply Chain Management System is a comprehensive application designed to manage and optimize the supply chain processes within a manufacturing and distribution network. This system integrates several components, including purchasing, delivery, warehouse management, and labor management, ensuring efficient and effective operations.

## Features

### Purchase Management (`purchasemanager.py`)
- **Material and Supplier Management**: Define materials and suppliers, including their prices and available quantities.
- **Factory Orders**: Manage raw material orders from factories.
- **Purchase Orders**: Create and track purchase orders, ensuring adequate supply of raw materials.
- **Database Integration**: Store and retrieve data using a MySQL database.

### Delivery Management (`deliverymanager.py`)
- **Producer and Warehouse Management**: Manage producers and warehouses, including their stock levels.
- **Deliver Orders**: Create and manage delivery orders from producers to warehouses.
- **Database Integration**: Update stock levels in the database after deliveries.

### Warehouse Management (`warehouse.py`)
- **Stock Display**: View current stock levels in warehouses.
- **Stock Adjustment**: Subtract stock from warehouses based on usage.
- **Add Requests**: Add additional stock when levels are low, integrating with the delivery management system.
- **Database Integration**: Retrieve and update warehouse stock data from the database.

### Labor Management (`labors.py`)
- **Employee Login**: Allow employees to log in and view their work data.
- **Work Status Tracking**: Display pending and completed work for employees.
- **Salary Status**: Indicate salary status based on the completion of pending work.
- **Database Integration**: Authenticate employees and retrieve their work data from the database.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/zorohack03/Supplychain-Management-version1.git
    ```
2. Navigate to the project directory:
    ```bash
    cd supply-chain-management-system
    ```
3. Install required dependencies:
    ```bash
    pip install mysql-connector-python
    ```
4. Set up your MySQL database:
    - Create a database named `supply_chain_management`.
    - Create necessary tables (`factories`, `supplier`, `producer`, `warehouse`, `employees`).
    - Populate the tables with initial data as needed.

## Usage

1. **Supplychain Management**:
    - Run `supply chain management system.py` to start the supply chain management interface.
    ```bash
    python supply chain management system.py
    ```
    
2. **Purchase Management**:
    - Run `purchasemanager.py` to start the purchase management interface.
    ```bash
    python purchasemanager.py
    ```

3. **Delivery Management**:
    - Run `deliverymanager.py` to start the delivery management interface.
    ```bash
    python deliverymanager.py
    ```

4. **Warehouse Management**:
    - Run `warehouse.py` to start the warehouse management interface.
    ```bash
    python warehouse.py
    ```

5. **Labor Management**:
    - Run `labors.py` to start the labor management interface.
    ```bash
    python labors.py
    ```

6. **Database**:
    - Run `supply_chain_management.sql` to get the mysql commands in mysql workbench.
    
## Components and GUI

- The application uses Tkinter for the graphical user interface.
- **Purchase Management**: GUI for creating and managing purchase orders.
- **Delivery Management**: GUI for managing delivery orders.
- **Warehouse Management**: GUI for displaying and adjusting warehouse stock levels.
- **Labor Management**: GUI for employees to check work status and salary information.

## Database Schema

Ensure your database schema matches the following structure:
- `factories`: Columns for  `id`, `name`, `raw_material`.
- `producer`: Columns for  `id`,`name`, `productA_quantity`, `productB_quantity`.
- `warehouse`: Columns for `id`, `product_id`, `product_name`, `price`, `quantity`.
- `employees`: Columns for `name`, `password`, `pending_work`, `completed_work`,`username`,`password` .

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests for any improvements or new features.


---

The README provides a comprehensive overview of the Supply Chain Management System, its features, and how to get started with the project. For any further assistance, please contact the us.


