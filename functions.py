import mysql.connector

mydb = mysql.connector.connect(
    host="sql5.freesqldatabase.com",
    port =3306,
    user="sql5675113",
    password="X4YdRtGYWm",
    database="sql5675113"
)

cursor = mydb.cursor()


def createTables():
    cursor.execute("""CREATE TABLE Product_category(
                    ProductCategoryID varchar(20) NOT NULL PRIMARY KEY,
                    CategoryName varchar(20));""")

    mydb.commit()
    cursor.execute("""CREATE TABLE Address1(
                            StreetName varchar(20) NOT NULL PRIMARY KEY,
                            PostalCode varchar(20),
                            StreetNumber varchar(20));""")
    mydb.commit()
    cursor.execute("""CREATE TABLE Address2(
                    AddressID varchar(20) NOT NULL PRIMARY KEY,
                    StreetName varchar(20),
                    StreetNumber varchar(20),
                    FOREIGN KEY (StreetName) REFERENCES Address1(StreetName));""")
    mydb.commit()
    cursor.execute("""CREATE TABLE Admin
            (UserID varchar(20) NOT NULL PRIMARY KEY,
            UserName varchar(20),
            UserPassword varchar(8)
            );""")
    mydb.commit()
    cursor.execute(""" CREATE TABLE customer
    (
                CustomerID varchar(20) NOT NULL PRIMARY KEY,
                CustomerName varchar(40),
                addressID varchar(20) NOT NULL,
                Email varchar(40) NOT NULL,
                DateOfBirth date,
                PhoneNum varchar(20),
                FOREIGN KEY (addressID) REFERENCES Address2(AddressID)
            );""")
    mydb.commit()
    cursor.execute("""CREATE TABLE Supplier1 (
            SupplierID varchar(20) PRIMARY KEY,
            Surname VARCHAR(255) NOT NULL,
            Contact VARCHAR(255) NOT NULL
        );""")
    mydb.commit()
    cursor.execute("""CREATE TABLE Supplier2 (
            SupplierID varchar(20) PRIMARY KEY,
            addressID varchar(20) NOT NULL,
            FOREIGN KEY (addressID) REFERENCES Address1(StreetName)
        );""")
    mydb.commit()
    cursor.execute("""CREATE TABLE test(
                       testid varchar(20) NOT NULL PRIMARY KEY);""")

    mydb.commit()
    cursor.execute("""CREATE TABLE Inventory 
        ( 
        inventoryID varchar(20) NOT NULL PRIMARY KEY, 
        Quantity int
        );""")
    mydb.commit()
    cursor.execute("""CREATE TABLE Product 
        ( 
        ProductID varchar(12) NOT NULL PRIMARY KEY,
        ProductName varchar(30),
        Price int,
        ProductCategoryID varchar(20) NOT NULL,
        inventoryID varchar(20) NOT NULL,
        FOREIGN KEY (ProductCategoryID) REFERENCES Product_category(ProductCategoryID),
        FOREIGN KEY (inventoryID) REFERENCES Inventory(inventoryID)
        );
        """)
    mydb.commit()
    cursor.execute("""CREATE TABLE Invoice -- already in 3NF
        (
        InvoiceId varchar(20) NOT NULL PRIMARY KEY,
        Total int NOT NULL,
        PaymentType varchar(12) NOT NULL,
        Date date NOT NULL,
        CustomerID varchar(20),
        FOREIGN KEY (CustomerID) REFERENCES customer(CustomerID)
        );""")
    mydb.commit()
    cursor.execute("""CREATE table Purchase_order -- already in 3NF
        (
        PurchaseID varchar(20) NOT NULL PRIMARY KEY,
        Date date,
        Quantity int,
        supplier_price int,
        Subtotal_Supplier int NOT NULL,
        SupplierID varchar(20),
        InvoiceID varchar(20),
        ProductID varchar(12),
        FOREIGN KEY (SupplierID) REFERENCES Supplier1(SupplierID),
        FOREIGN KEY (InvoiceID) REFERENCES Invoice(InvoiceId),
        FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
        );""")
    mydb.commit()
    cursor.execute("""CREATE TABLE SalesOrder1 (
      SalesID varchar(20) PRIMARY KEY,
      Quantity_sold INT NOT NULL,
      Subtotal DECIMAL(10,2) NOT NULL
    );""")
    mydb.commit()
    cursor.execute("""CREATE TABLE SalesOrder2 (
      SalesID varchar(20) PRIMARY KEY,
      ProductID varchar(20) NOT NULL,
      FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
    );""")


def populate_table():
    cursor.execute("""INSERT INTO Product_category (ProductCategoryID, CategoryName) VALUES
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
    cursor.execute("""INSERT INTO Address1 (StreetName, PostalCode, StreetNumber) VALUES
                                ('Main Rd', 'M4R 9D0', '345'),
                                ('Main Street', 'J3X 0M1', '298'),
                                ('Main Ave', 'L3L 3P7', '099'); """)
    mydb.commit()
    cursor.execute("""INSERT INTO Address2 (AddressID, StreetName, StreetNumber) VALUES
                                    ('A001', 'Main Rd', '345'),
                                    ('A002', 'Main Street', '298'),
                                    ('A003', 'Main Ave', '099'); """)
    mydb.commit()


    cursor.execute("""INSERT INTO Admin (UserID, UserName, UserPassword) VALUES
            ('UID001', 'Bob', '123'),
            ('UID002', 'Bobby', '321'),
            ('UID003', 'Bobber', '12321'); """)

    mydb.commit()


    cursor.execute("""INSERT INTO customer (CustomerID, CustomerName, addressID, Email, DateOfBirth, PhoneNum) VALUES
                        ('C005', 'BOB', 'A001','bob@example.com', '1969-04-01', '123-456-7890'),
                        ('C001', 'Inder', 'A002', 'inder@example.com', '2002-03-27', '123-456-7890'),
                        ('C002', 'Manan', 'A003', 'manan@example.com', '2002-02-12', '234-567-8901'),
                        ('C003', 'Inder', 'A001', 'inder@example.com', '2002-03-27', '123-456-7890'),
                        ('C004', 'Ama', 'A003', 'ama@example.com', '2002-02-13', '345-678-9012'); """)
    mydb.commit()

    cursor.execute("""INSERT INTO Supplier1 (SupplierID, Surname, Contact) VALUES
                    ('SID001', 'Smith', '111-111-1111'),
                    ('SID002', 'Johnson', '222-222-2222'),
                    ('SID003', 'Williams', '333-333-3333');""")
    mydb.commit()


    cursor.execute("""INSERT INTO Supplier2 (SupplierID, addressID) VALUES
                    ('SID001', 'Main Rd'),
                    ('SID002', 'Main Rd'),
                    ('SID003', 'Main Rd');""")
    mydb.commit()
    cursor.execute("""INSERT INTO Inventory (inventoryID, Quantity) VALUES
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

    cursor.execute("""INSERT INTO Product (ProductID, ProductName, Price, ProductCategoryID, inventoryID) VALUES 
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

    cursor.execute("""INSERT INTO Invoice (InvoiceId, Total, PaymentType, Date, CustomerID) VALUES
            ('IN00001', 100, 'Credit Card', '2023-01-01', 'C001'),
            ('IN00002', 200, 'Debit Card', '2023-01-02', 'C002'),
            ('IN00003', 300, 'Cash', '2023-01-03', 'C003');   """)
    mydb.commit()

    cursor.execute("""INSERT INTO Purchase_order (PurchaseID, Date, Quantity, supplier_price, Subtotal_Supplier, SupplierID, InvoiceID, ProductID) VALUES
        ('PO-0001', '2022-01-01', 10, 1000, 2000,'SID001', 'IN00001', 'PR001'),
        ('PO-0002', '2022-02-01', 20, 2000, 2000,'SID002', 'IN00002', 'PR002'),
        ('PO-0003', '2022-03-01', 30, 3000, 2000,'SID003', 'IN00003', 'PR003');""")
    mydb.commit()

    cursor.execute("""INSERT INTO SalesOrder1 (SalesID, Quantity_sold, Subtotal) VALUES
        ('S001', 5, 50),
        ('S002', 10, 100),
        ('S003', 15, 150);""")
    mydb.commit()

    cursor.execute("""INSERT INTO SalesOrder2 (SalesID, ProductID) VALUES
        ('S001', 'PR001'),
        ('S002', 'PR002'),
        ('S003', 'PR003');""")
    mydb.commit()




# -------------------------------------------------------------------------
# Read table
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


def view(sg):
    layout = [[sg.Text('Table includes')]]
    for x in cursor:
        layout.append([sg.Text(x)])
    sg.theme('DarkAmber')  # Set theme
    window = sg.Window('Table', layout)
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Close':
        window.close()


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
        sql = "DROP TABLE " + values[0]
        cursor.execute(sql)
        window.close()


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


def delte_helper(sg, table, identity):
    sg.theme('DarkAmber')
    layout = [[sg.Text(f'Enter {identity}'), sg.InputText()],
              [sg.Button('Submit'), sg.Button('Close')]]
    window = sg.Window('Delete', layout)
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Close':
        window.close()
    elif table == "Admin":
        sql = "DELETE FROM " + table + " WHERE Username= \'" + values[0] + "\'"
    elif table == "Inventory":
        sql = "DELETE FROM " + table + " WHERE ProductID= \'" + values[0] + "\'"
    elif table == "saleOrder1" or table == "saleOrder2":
        sql = "DELETE FROM " + table + " WHERE SalesID= \'" + values[0] + "\'"
    elif table == "Purchase_order":
        sql = "DELETE FROM " + table + " WHERE PurchaseID= \'" + values[0] + "\'"
    elif table == "Product":
        sql = "DELETE FROM " + table + " WHERE ProductName= \'" + values[0] + "\'"
    elif table == "Invoice":
        sql = "DELETE FROM " + table + " WHERE InvoiceId= \'" + values[0] + "\'"
    elif table == "Supplier1":
        sql = "DELETE FROM " + table + " WHERE Surname= \'" + values[0] + "\'"
    elif table == "Supplier2":
        sql = "DELETE FROM " + table + " WHERE SupplierID= \'" + values[0] + "\'"
    elif table == "Product_category":
        sql = "DELETE FROM " + table + " WHERE ProductCategoryID= \'" + values[0] + "\'"
    elif table == "customer":
        sql = "DELETE FROM " + table + " WHERE CustomerName= \'" + values[0] + "\'"
    cursor.execute(sql)
    window.close()


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


def search_helper(sg, table, identity):
    sg.theme('DarkAmber')
    layout = [[sg.Text(f'Enter {identity}'), sg.InputText()],
              [sg.Button('Submit'), sg.Button('Close')]]
    window = sg.Window('Search', layout)
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Close':
        window.close()
    elif table == "Admin":
        sql = "SELECT * FROM " + table + " WHERE Username= \'" + values[0] + "\'"
    elif table == "Inventory":
        sql = "SELECT * FROM " + table + " WHERE ProductID= \'" + values[0] + "\'"
    elif table == "sales":
        sql = "SELECT * FROM " + table + " WHERE SalesID= \'" + values[0] + "\'"
    elif table == "Purchase_order":
        sql = "SELECT * FROM " + table + " WHERE PurchaseID= \'" + values[0] + "\'"
    elif table == "Product":
        sql = "SELECT * FROM " + table + " WHERE ProductName= \'" + values[0] + "\'"
    elif table == "Invoice":
        sql = "SELECT * FROM " + table + " WHERE InvoiceId= \'" + values[0] + "\'"
    elif table == "Supplier":
        sql = "SELECT * FROM " + table + " WHERE Surname= \'" + values[0] + "\'"
    elif table == "Product_category":
        sql = "SELECT * FROM " + table + " WHERE ProductCategoryID= \'" + values[0] + "\'"
    elif table == "customer":
        sql = "SELECT * FROM " + table + " WHERE CustomerName= \'" + values[0] + "\'"
    cursor.execute(sql)
    view(sg)
    window.close()


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


def update1(sg, table):
    sg.theme('DarkAmber')
    layout = [[sg.Text(f'Select old CustomerName for {table}'), sg.InputText()],
              [sg.Text(f'Select new CustomerName for {table}'), sg.InputText()],
              [sg.Text(f'Select new PhoneNum for {table}'), sg.InputText()],
              [sg.Text(f'Select new email for {table}'), sg.InputText()],
              [sg.Button('Submit')]]
    window = sg.Window('Update Table', layout)
    event, values = window.read()
    sql = "UPDATE " + table + " SET CustomerName =\'" + values[1] + "\', PhoneNum=\'" + values[2] + "\',email = \'" + \
          values[3] + "\' WHERE CustomerName= \'" + values[0] + "\'"
    cursor.execute(sql)
    window.close()
