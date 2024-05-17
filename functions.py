import sqlite3
import time
import uuid

# Connect to SQLite database (it will create the database file if it doesn't exist)
mydb = sqlite3.connect('mydatabase.db', check_same_thread=False)
cursor = mydb.cursor()


def retry_on_locked(func):
    def wrapper(*args, **kwargs):
        retries = 5
        delay = 1
        for i in range(retries):
            try:
                return func(*args, **kwargs)
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e):
                    time.sleep(delay)
                    delay *= 2
                else:
                    raise
        raise sqlite3.OperationalError("database is locked after several retries")
    return wrapper


@retry_on_locked
def createTables():
    cursor.execute("""CREATE TABLE IF NOT EXISTS Product_category(
                    ProductCategoryID TEXT NOT NULL PRIMARY KEY,
                    CategoryName TEXT);""")

    mydb.commit()
    cursor.execute("""CREATE TABLE IF NOT EXISTS Address1(
                            StreetName TEXT NOT NULL PRIMARY KEY,
                            PostalCode TEXT,
                            StreetNumber TEXT);""")
    mydb.commit()
    cursor.execute("""CREATE TABLE IF NOT EXISTS Address2(
                    AddressID TEXT NOT NULL PRIMARY KEY,
                    StreetName TEXT,
                    StreetNumber TEXT,
                    FOREIGN KEY (StreetName) REFERENCES Address1(StreetName));""")
    mydb.commit()
    cursor.execute("""CREATE TABLE IF NOT EXISTS Admin
            (UserID TEXT NOT NULL PRIMARY KEY,
            UserName TEXT,
            UserPassword TEXT
            );""")
    mydb.commit()
    cursor.execute(""" CREATE TABLE IF NOT EXISTS customer
    (
                CustomerID TEXT NOT NULL PRIMARY KEY,
                CustomerName TEXT,
                addressID TEXT NOT NULL,
                Email TEXT NOT NULL,
                DateOfBirth DATE,
                PhoneNum TEXT,
                FOREIGN KEY (addressID) REFERENCES Address2(AddressID)
            );""")
    mydb.commit()
    cursor.execute("""CREATE TABLE IF NOT EXISTS Supplier1 (
            SupplierID TEXT PRIMARY KEY,
            Surname TEXT NOT NULL,
            Contact TEXT NOT NULL
        );""")
    mydb.commit()
    cursor.execute("""CREATE TABLE IF NOT EXISTS Supplier2 (
            SupplierID TEXT PRIMARY KEY,
            addressID TEXT NOT NULL,
            FOREIGN KEY (addressID) REFERENCES Address1(StreetName)
        );""")
    mydb.commit()
    cursor.execute("""CREATE TABLE IF NOT EXISTS test(
                       testid TEXT NOT NULL PRIMARY KEY);""")

    mydb.commit()
    cursor.execute("""CREATE TABLE IF NOT EXISTS Inventory 
        ( 
        inventoryID TEXT NOT NULL PRIMARY KEY, 
        Quantity INTEGER
        );""")
    mydb.commit()
    cursor.execute("""CREATE TABLE IF NOT EXISTS Product 
        ( 
        ProductID TEXT NOT NULL PRIMARY KEY,
        ProductName TEXT,
        Price REAL,
        ProductCategoryID TEXT NOT NULL,
        inventoryID TEXT NOT NULL,
        FOREIGN KEY (ProductCategoryID) REFERENCES Product_category(ProductCategoryID),
        FOREIGN KEY (inventoryID) REFERENCES Inventory(inventoryID)
        );
        """)
    mydb.commit()
    cursor.execute("""CREATE TABLE IF NOT EXISTS Invoice -- already in 3NF
        (
        InvoiceId TEXT NOT NULL PRIMARY KEY,
        Total INTEGER NOT NULL,
        PaymentType TEXT NOT NULL,
        Date DATE NOT NULL,
        CustomerID TEXT,
        FOREIGN KEY (CustomerID) REFERENCES customer(CustomerID)
        );""")
    mydb.commit()
    cursor.execute("""CREATE table IF NOT EXISTS Purchase_order -- already in 3NF
        (
        PurchaseID TEXT NOT NULL PRIMARY KEY,
        Date DATE,
        Quantity INTEGER,
        supplier_price INTEGER,
        Subtotal_Supplier INTEGER NOT NULL,
        SupplierID TEXT,
        InvoiceID TEXT,
        ProductID TEXT,
        FOREIGN KEY (SupplierID) REFERENCES Supplier1(SupplierID),
        FOREIGN KEY (InvoiceID) REFERENCES Invoice(InvoiceId),
        FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
        );""")
    mydb.commit()
    cursor.execute("""CREATE TABLE IF NOT EXISTS SalesOrder1 (
      SalesID TEXT PRIMARY KEY,
      Quantity_sold INTEGER NOT NULL,
      Subtotal REAL NOT NULL
    );""")
    mydb.commit()
    cursor.execute("""CREATE TABLE IF NOT EXISTS SalesOrder2 (
      SalesID TEXT PRIMARY KEY,
      ProductID TEXT NOT NULL,
      Quantity INTEGER NOT NULL,
      Price REAL NOT NULL,
      FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
    );""")
    mydb.commit()


@retry_on_locked
def populate_table():
    cursor.execute("""INSERT OR IGNORE INTO Product_category (ProductCategoryID, CategoryName) VALUES
                        ('PC001', 'Home & Electronics'),
                        ('PC002', 'Health & Wellness'),
                        ('PC003', 'Prescriptions'),
                        ('PC004', 'Groceries'),
                        ('PC005', 'Clothing'),
                        ('PC006', 'Toys & Games'),
                        ('PC007', 'Books'),
                        ('PC008', 'Sports'),
                        ('PC009', 'Office Supplies'),
                        ('PC010', 'Gardening Tools'),
                        ('PC011', 'Beauty Products'),
                        ('PC012', 'Footwear'),
                        ('PC013', 'Jewelry'),
                        ('PC014', 'Automotive'),
                        ('PC015', 'Pet Supplies'); """)
    mydb.commit()
    cursor.execute("""INSERT OR IGNORE INTO Address1 (StreetName, PostalCode, StreetNumber) VALUES
                                ('Main Rd', 'M4R 9D0', '345'),
                                ('Main Street', 'J3X 0M1', '298'),
                                ('Main Ave', 'L3L 3P7', '099'); """)
    mydb.commit()
    cursor.execute("""INSERT OR IGNORE INTO Address2 (AddressID, StreetName, StreetNumber) VALUES
                                    ('A001', 'Main Rd', '345'),
                                    ('A002', 'Main Street', '298'),
                                    ('A003', 'Main Ave', '099'); """)
    mydb.commit()


    cursor.execute("""INSERT OR IGNORE INTO Admin (UserID, UserName, UserPassword) VALUES
            ('UID001', 'Bob', '123'),
            ('UID002', 'Bobby', '321'),
            ('UID003', 'Bobber', '12321'); """)

    mydb.commit()


    cursor.execute("""INSERT OR IGNORE INTO customer (CustomerID, CustomerName, addressID, Email, DateOfBirth, PhoneNum) VALUES
                        ('C005', 'BOB', 'A001','bob@example.com', '1969-04-01', '123-456-7890'),
                        ('C001', 'Inder', 'A002', 'inder@example.com', '2002-03-27', '123-456-7890'),
                        ('C002', 'Manan', 'A003', 'manan@example.com', '2002-02-12', '234-567-8901'),
                        ('C003', 'Inder', 'A001', 'inder@example.com', '2002-03-27', '123-456-7890'),
                        ('C004', 'Ama', 'A003', 'ama@example.com', '2002-02-13', '345-678-9012'); """)
    mydb.commit()

    cursor.execute("""INSERT OR IGNORE INTO Supplier1 (SupplierID, Surname, Contact) VALUES
                    ('SID001', 'Smith', '111-111-1111'),
                    ('SID002', 'Johnson', '222-222-2222'),
                    ('SID003', 'Williams', '333-333-3333');""")
    mydb.commit()


    cursor.execute("""INSERT OR IGNORE INTO Supplier2 (SupplierID, addressID) VALUES
                    ('SID001', 'Main Rd'),
                    ('SID002', 'Main Rd'),
                    ('SID003', 'Main Rd');""")
    mydb.commit()
    cursor.execute("""INSERT OR IGNORE INTO Inventory (inventoryID, Quantity) VALUES
    ('INV01', 100),
    ('INV02', 200),
    ('INV03', 300),
    ('INV04', 150),
    ('INV05', 100),
    ('INV06', 250),
    ('INV07', 250),
    ('INV08', 100),
    ('INV09', 120),
    ('INV10', 150),
    ('INV11', 80),
    ('INV12', 60),
    ('INV13', 100),
    ('INV14', 200),
    ('INV15', 150);
 """)
    mydb.commit()

    cursor.execute("""INSERT OR IGNORE INTO Product (ProductID, ProductName, Price, ProductCategoryID, inventoryID) VALUES 
    ('PR001', 'Iphone', 1200, 'PC001', 'INV01'),
    ('PR002', 'Toothbrush', 25.3, 'PC002', 'INV02'),
    ('PR003', 'Mirror', 45.50, 'PC003', 'INV03'),
    ('PR004', 'Laptop', 800, 'PC001', 'INV04'),
    ('PR005', 'Speaker', 150, 'PC001', 'INV05'),
    ('PR006', 'Vitamins', 30, 'PC002', 'INV06'),
    ('PR007', 'Pain Reliever', 20, 'PC002', 'INV07'),
    ('PR008', 'Book "Sapiens"', 20, 'PC007', 'INV08'),
    ('PR009', 'Running Shoes', 100, 'PC008', 'INV09'),
    ('PR010', 'Yoga Mat', 50, 'PC008', 'INV10'),
    ('PR011', 'Desk Lamp', 45, 'PC009', 'INV11'),
    ('PR012', 'Office Chair', 200, 'PC009', 'INV12'),
    ('PR013', 'Gardening Shovel', 35, 'PC010', 'INV13'),
    ('PR014', 'Plant Fertilizer', 15, 'PC010', 'INV14'),
    ('PR015', 'Dog Leash', 20, 'PC015', 'INV15');
 """)
    mydb.commit()



    cursor.execute("""INSERT OR IGNORE INTO Purchase_order (PurchaseID, Date, Quantity, supplier_price, Subtotal_Supplier, SupplierID, InvoiceID, ProductID) VALUES
        ('PO-0001', '2022-01-01', 10, 1000, 2000,'SID001', 'IN00001', 'PR001'),
        ('PO-0002', '2022-02-01', 20, 2000, 2000,'SID002', 'IN00002', 'PR002'),
        ('PO-0003', '2022-03-01', 30, 3000, 2000,'SID003', 'IN00003', 'PR003');""")
    mydb.commit()

    cursor.execute("""INSERT OR IGNORE INTO SalesOrder1 (SalesID, Quantity_sold, Subtotal) VALUES
        ('S001', 5, 50),
        ('S002', 10, 100),
        ('S003', 15, 150);""")
    mydb.commit()



# -------------------------------------------------------------------------
# Read table
@retry_on_locked
def view_table(sg):
    sg.theme('DarkAmber')
    layout = [[sg.Text('Please enter the table name to view')],
              [sg.Text('Table Name'), sg.InputText()],
              [sg.Button('View'), sg.Button('Close')]]
    window = sg.Window('Read Table', layout)
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Close':
        window.close()
    else:
        sql = "SELECT * FROM " + values[0]
        cursor.execute(sql)
        view(sg)
        window.close()


@retry_on_locked
def view(sg):
    layout = [[sg.Text('Table includes')]]
    for x in cursor:
        layout.append([sg.Text(x)])
    sg.theme('DarkAmber')  # Set theme
    window = sg.Window('Table', layout)
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Close':
        window.close()


@retry_on_locked
def drop_table(sg):
    sg.theme('DarkAmber')
    layout = [[sg.Text('Please enter the table to be dropped')],
              [sg.Text("""Tables: Tables: [Admin, Inventory, salesorder1,salesorder2,Purchase_order,Product,
                   Invoice,Supplier1,Supplier2,Product_category,customer]""")],
              [sg.Text('Table Name'), sg.InputText()],
              [sg.Button('Drop'), sg.Button('Close')]]
    window = sg.Window('Menu', layout)
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Close':
        window.close()
    else:
        sql = "DROP TABLE IF EXISTS " + values[0]
        cursor.execute(sql)
        window.close()


@retry_on_locked
def delete(sg):
    sg.theme('DarkAmber')
    layout = [[sg.Text('Please select the table to delete from')],
              [sg.Text(
                  """Tables: [Admin, Inventory, salesorder1,salesorder2,Purchase_order,Product,
                   Invoice,Supplier1,Supplier2,Product_category,customer]""")],
              [sg.Text('Table Name'), sg.InputText()],
              [sg.Button('Submit'), sg.Button('Close')]]
    window = sg.Window('Delete', layout)
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Close':
        window.close()
    elif values[0] == "Admin":
        delte_helper(sg, "Admin", "Username")
    elif values[0] == "Inventory":
        delte_helper(sg, "Inventory", "inventoryID")
    elif values[0] == "Purchase_order":
        delte_helper(sg, "Purchase_order", "PurchaseID")
    elif values[0] == "Product":
        delte_helper(sg, "Product", "ProductName")
    elif values[0] == "Invoice":
        delte_helper(sg, "Invoice", "InvoiceId")
    elif values[0] == "Supplier1":
        delte_helper(sg, "Supplier1", "Surname")
    elif values[0] == "Supplier2":
        delte_helper(sg, "Supplier2", "SupplierID")
    elif values[0] == "salesOrder1":
        delte_helper(sg, "salesOrder1", "SalesID")
    elif values[0] == "salesOrder2":
        delte_helper(sg, "salesOrder2", "SalesID")
    elif values[0] == "Product_category":
        delte_helper(sg, "Product_category", "ProductCategoryID")
    elif values[0] == "customer":
        delte_helper(sg, "customer", "CustomerName")

    sg.popup(' Record Deleted.')
    window.close()


@retry_on_locked
def delte_helper(sg, table, identity):
    sg.theme('DarkAmber')
    layout = [[sg.Text(f'Enter {identity}'), sg.InputText()],
              [sg.Button('Submit'), sg.Button('Close')]]
    window = sg.Window('Delete', layout)
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Close':
        window.close()
    sql = "DELETE FROM " + table + " WHERE " + identity + " = ?"
    cursor.execute(sql, (values[0],))
    mydb.commit()
    window.close()


@retry_on_locked
def search(sg):
    sg.theme('DarkAmber')
    layout = [[sg.Text('Please select the table to be searched from')],
              [sg.Text(
                  """Tables: [Admin, Inventory, salesorder1,salesorder2,Purchase_order,Product,
                   Invoice,Supplier1,Supplier2,Product_category,customer]""")],
              [sg.Text('Table Name'), sg.InputText()],
              [sg.Button('Submit'), sg.Button('Close')]]
    window = sg.Window('Menu', layout)
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Close':
        window.close()
    elif values[0] == "Admin":
        search_helper(sg, "Admin", "Username")
    elif values[0] == "Inventory":
        search_helper(sg, "Inventory", "ProductID")
    elif values[0] == "Purchase_order":
        search_helper(sg, "Purchase_order", "PurchaseID")
    elif values[0] == "Product":
        search_helper(sg, "Product", "ProductName")
    elif values[0] == "Invoice":
        search_helper(sg, "Invoice", "InvoiceId")
    elif values[0] == "Supplier1":
        search_helper(sg, "Supplier1", "Surname")
    elif values[0] == "Supplier2":
        search_helper(sg, "Supplier2", "SupplierID")
    elif values[0] == "salesOrder1":
        search_helper(sg, "salesOrder1", "SalesID")
    elif values[0] == "salesOrder2":
        search_helper(sg, "salesOrder2", "SalesID")
    elif values[0] == "Product_category":
        search_helper(sg, "Product_category", "ProductCategoryID")
    elif values[0] == "customer":
        search_helper(sg, "customer", "CustomerName")


@retry_on_locked
def search_helper(sg, table, identity):
    sg.theme('DarkAmber')
    layout = [[sg.Text(f'Enter {identity}'), sg.InputText()],
              [sg.Button('Submit'), sg.Button('Close')]]
    window = sg.Window('Search', layout)
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Close':
        window.close()
    sql = "SELECT * FROM " + table + " WHERE " + identity + " = ?"
    cursor.execute(sql, (values[0],))
    view(sg)
    window.close()


@retry_on_locked
def update(sg):
    sg.theme('DarkAmber')
    layout = [[sg.Text(f'Enter table '), sg.InputText()],
              [sg.Button('Submit'), sg.Button('Close')]]
    window = sg.Window('Update Table', layout)
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Close':
        window.close()
    window.close()
    update1(sg, values[0])


@retry_on_locked
def update1(sg, table):
    sg.theme('DarkAmber')
    layout = [[sg.Text(f'Select old CustomerName for {table}'), sg.InputText()],
              [sg.Text(f'Select new CustomerName for {table}'), sg.InputText()],
              [sg.Text(f'Select new PhoneNum for {table}'), sg.InputText()],
              [sg.Text(f'Select new email for {table}'), sg.InputText()],
              [sg.Button('Submit')]]
    window = sg.Window('Update Table', layout)
    event, values = window.read()
    sql = "UPDATE " + table + " SET CustomerName = ?, PhoneNum = ?, email = ? WHERE CustomerName = ?"
    cursor.execute(sql, (values[1], values[2], values[3], values[0]))
    mydb.commit()
    window.close()


@retry_on_locked
def fetch_past_sales():
    past_sales = []
    try:
        cursor.execute("SELECT InvoiceId, Date FROM Invoice ORDER BY Date DESC")
        results = cursor.fetchall()
        for row in results:
            # Format the sales summary as needed
            sale_summary = f"Invoice ID: {row[0]}, Date: {row[1]}"
            past_sales.append(sale_summary)
    except sqlite3.Error as err:
        print("Error occurred: ", err)
    return past_sales

@retry_on_locked
def get_receipt_for_sale(sale_summary):
    # Extract InvoiceId from the sale_summary
    invoice_id = sale_summary.split(",")[0].split(":")[1].strip()

    receipt = "----- Receipt -----\n"
    try:
        # Fetch sale details from the database
        cursor.execute("SELECT ProductID, Quantity, Price FROM SalesOrder2 WHERE SalesID = ?", (invoice_id,))
        results = cursor.fetchall()

        total_cost = 0
        for product_id, quantity, price in results:
            cost = quantity * price
            total_cost += cost
            receipt += f"Product ID: {product_id}, Quantity: {quantity}, Unit Price: ${price}, Cost: ${cost}\n"

        receipt += f"Total Cost: ${total_cost}\n"
        receipt += "------------------\n"
    except sqlite3.Error as err:
        print("Error occurred: ", err)
        receipt += "Error in generating receipt\n"
    
    return receipt


@retry_on_locked
def generate_invoice_id():
    return str(uuid.uuid4())

@retry_on_locked
def save_invoice(total_cost, payment_type, customer_id=None):
    invoice_id = generate_invoice_id()
    date = time.strftime('%Y-%m-%d')
    
    cursor.execute("""INSERT INTO Invoice (InvoiceId, Total, PaymentType, Date, CustomerID) VALUES (?, ?, ?, ?, ?)""",
                   (invoice_id, total_cost, payment_type, date, customer_id))
    mydb.commit()
    return invoice_id

@retry_on_locked
def save_sales_order(invoice_id, product_id, quantity, price):
    sales_id = generate_invoice_id()
    cursor.execute("""INSERT INTO SalesOrder2 (SalesID, ProductID, Quantity, Price) VALUES (?, ?, ?, ?)""",
                   (sales_id, product_id, quantity, price))
    mydb.commit()