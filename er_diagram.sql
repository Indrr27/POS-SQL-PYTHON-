USE er_diagram; /* er_diagram is my schema name. Make sure to write yours instead before running the code*/

CREATE TABLE Product_category -- already in 3NF
(
ProductCategoryID varchar(20) NOT NULL PRIMARY KEY,
CategoryName varchar(20)
);

CREATE TABLE Admin -- already in 3NF
(
UserID varchar(20) NOT NULL PRIMARY KEY,
UserName varchar(20),
UserPassword varchar(8)
);
CREATE TABLE address -- Already in 3NF 
(
AddressID varchar(20) NOT NULL PRIMARY KEY,
StreetName varchar(40) NOT NULL, 
StreetNumber varchar(40) NOT NULL, 
PostalCode varchar(8)
);

CREATE TABLE customer -- Already in 3NF 
(
CustomerID varchar(20) NOT NULL PRIMARY KEY,
addressID varchar(20) NOT NULL, 
CustomerName varchar(40),
Email varchar(40) NOT NULL,
DateOfBirth date,
PhoneNum varchar(20),
FOREIGN KEY (AddressID) REFERENCES adress(AddressID)
);

CREATE TABLE Supplier -- Already in 3NF 
(
SupplierID varchar(20) NOT NULL PRIMARY KEY,
addressID varchar(20) NOT NULL, -- NEW
Supname varchar(20),
Contact VARCHAR(12) DEFAULT '416-979-500',
FOREIGN KEY (AddressID) REFERENCES adress(AddressID)
);

CREATE TABLE Inventory -- Already in 3NF 
( 
inventoryID varchar(20) NOT NULL PRIMARY KEY, 
Quantity int
);

CREATE TABLE Product -- Already in 3NF 
( 
ProductID varchar(12) NOT NULL PRIMARY KEY,
inventoryID varchar(20) NOT NULL,
ProductName varchar(30),
Price int,
ProductCategoryID varchar(20),
FOREIGN KEY (ProductCategoryID) REFERENCES Product_category(ProductCategoryID),
FOREIGN KEY (inventoryID) REFERENCES Inventory(inventoryID)
);

CREATE TABLE Invoice -- already in 3NF
(
InvoiceId varchar(20) NOT NULL PRIMARY KEY,
Total int NOT NULL,
PaymentType varchar(12) NOT NULL,
Date date NOT NULL,
CustomerID varchar(20),
FOREIGN KEY (CustomerID) REFERENCES customer(CustomerID)
);

CREATE table Purchase_order -- already in 3NF
(
PurchaseID varchar(20) NOT NULL PRIMARY KEY,
Date date,
Quantity int,
supplier_price int,
Subtotal_Supplier int NOT NULL,
SupplierID varchar(20),
InvoiceID varchar(20),
ProductID varchar(12),
FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID),
FOREIGN KEY (InvoiceID) REFERENCES Invoice(InvoiceId),
FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);

CREATE TABLE sales -- already in 3NF
(
SalesID varchar(20) NOT NULL PRIMARY KEY,
Quantity_sold int NOT NULL,
Subtotal int NOT NULL,
ProductID varchar(12),
InvoiceID varchar(20),
FOREIGN KEY (ProductID) REFERENCES Product(ProductID),
FOREIGN KEY (InvoiceID) REFERENCES Invoice(InvoiceId)
);

/*================================================================================================================================================== */ 

INSERT INTO address (AddressID, StreetName, StreetNumber, PostalCode) VALUES
('AID001', 'Downtown Rd', '123', 'L11 5M1'),
('AID002', 'Main Rd', '23', 'K13 5A1'),
('AID003', 'Low Rd', '333', 'P13 2Q1'),
('AID004', 'HighTown Ave', '456', 'N16 3M1'),
('AID005', 'Pearl Street', '678', 'K24 7J1'),
('AID006', 'Downtown Rd', '38', 'Q51 5H1');




INSERT INTO Product_category (ProductCategoryID, CategoryName) VALUES
('PC001', 'Home & Electronics'),
('PC002', 'Health & Wellness'),
('PC003', 'Prescriptions');

INSERT INTO Admin (UserID, UserName, UserPassword) VALUES
('UID001', 'Bob', '123'),
('UID002', 'Bobby', '321'),
('UID003', 'Bobber', '12321');

INSERT INTO Invoice (InvoiceId, Total, PaymentType, Date, CustomerID) VALUES
('IN00001', 100, 'Credit Card', '2023-01-01', 'C001'),
('IN00002', 200, 'Debit Card', '2023-01-02', 'C002'),
('IN00003', 300, 'Cash', '2023-01-03', 'C003'); 
















/* Populating Customer Table */ 
DELETE FROM Customers WHERE CustomerName='Alfreds Futterkiste';

SELECT DISTINCT CustomerName, Email, PhoneNum FROM customer /* Querying customer names, email and phonenumber */
ORDER BY CustomerName ASC;  -- Order products in desc order 
/*================================================================================================================================================== */ 
 
/* Populating Product category Table */ 
INSERT INTO Product_category (ProductCategoryID, CategoryName) VALUES
('PC001', 'Home & Electronics'),
('PC002', 'Health & Wellness'),
('PC003', 'Prescriptions');

SELECT CategoryName FROM Product_category; /* Querying Product categories and ids */

 /*================================================================================================================================================== */ 

/* Populating Admin Table */ 
-

SELECT DISTINCT UserID, UserName FROM Admin; /* Querying Admin for UserID and Username */

/*================================================================================================================================================== */ 

/* Populating Supplier Table */ 
INSERT INTO Supplier (SupplierID, Supname, Address, Contact) VALUES
('SID001', 'Bob Store', '123 Downtown Rd', '111-111-1111'),
('SID002', 'Bobby Store', '456 Downtown Rd', '222-222-2222'),
('SID003', 'Bobber Store', '789 Downtown Rd', '333-333-3333');

SELECT Supname, Contact FROM Supplier; /* Querying Supplier for Name and Contact */

/*================================================================================================================================================== */ 

/* Populating Invoice Table */ 



SELECT invoiceTable.InvoiceId, invoiceTable.Total, c.CustomerName FROM Invoice invoiceTable
JOIN customer c ON invoiceTable.CustomerID = c.CustomerID /* Querying Invoice for ID, Total, and CustomerName*/
ORDER BY Date DESC;  -- Order products in desc order 
/*================================================================================================================================================== */ 

/* Populating Product Table */ 
INSERT INTO Product (ProductID, ProductName, Quantity, Price, ProductCategoryID) VALUES 
('P007', 'ELECTRIC Toothbrush', 50, 200, 'PC002'),
('P006', 'Toothbrush', 50, 200, 'PC002'),
('P005', 'TV', 50, 1000, 'PC001'),
('P004', 'Keyboard', 50, 100, 'PC001'),
('P001', 'Headphones', 50, 100, 'PC001'),
('P002', 'Toothpaste', 30, 3, 'PC002'),
('P003', 'Advil', 20, 5, 'PC003');



SELECT ProductName, Quantity, Price, CategoryName FROM Product
JOIN Product_category ON Product.ProductCategoryID = Product_category.ProductCategoryID /* Querying Product for Name, quantity, price, and category name*/
ORDER BY Price DESC;  -- Order products in desc order 

/*================================================================================================================================================== */ 

/* Populating Purchase_order Table */ 
INSERT INTO Purchase_order (PurchaseID, Date, Quantity, Price, SupplierID, InvoiceID, ProductID) VALUES 
('PO-0001', '2022-01-01', 10, 1000, 'SID001', 'IN00001', 'P001'),
('PO-0002', '2022-02-01', 20, 2000, 'SID002', 'IN00002', 'P002'),
('PO-0003', '2022-03-01', 30, 3000, 'SID003', 'IN00003', 'P003');

SELECT Purchase_order.PurchaseID, Purchase_order.Date, Purchase_order.Quantity, Purchase_order.Price, Supplier.Supname, Invoice.Total, Product.ProductName FROM Purchase_order
JOIN Supplier ON Purchase_order.SupplierID = Supplier.SupplierID
JOIN Invoice ON Purchase_order.InvoiceID = Invoice.InvoiceId
JOIN Product ON Purchase_order.ProductID = Product.ProductID /* Querying purchase order*/
ORDER BY Price ASC;  -- Order products in desc order 
/*================================================================================================================================================== */ 

/* Populating Sales Table */ 
INSERT INTO sales (SalesID, Quantity, Subtotal, ProductID, InvoiceID) VALUES 
('S001', 10, 200, 'P001', 'IN00001'),
('S002', 5, 100, 'P002', 'IN00002'),
('S003', 8, 160, 'P003', 'IN00003');
       

SELECT s.SalesID, s.Quantity, s.Subtotal, p.ProductName, i.InvoiceId FROM sales s
JOIN Product p ON s.ProductID = p.ProductID
JOIN Invoice i ON s.InvoiceID = i.InvoiceId/* Querying Sales*/
ORDER BY Subtotal ASC;  -- Order products in desc order 
/*================================================================================================================================================== */ 

/* Populating Inventory Table */ 
INSERT INTO Inventory (ProductID, Quantity) VALUES 
('P001', 10), 
('P002', 5), 
('P003', 15);

SELECT i.ProductID, p.ProductName, p.ProductCategoryID, i.Quantity FROM Inventory i
JOIN Product p ON i.ProductID = p.ProductID; /* Querying Inventory*/

/*================================================================================================================================================== */ 
-- 7 advanced queries

SELECT ProductName, ProductCategoryID, Price from Product 
WHERE ProductCategoryID = 'PC001'
union
(SELECT ProductName, ProductCategoryID, Price from Product 
WHERE Price > 200);

-- Query using the NOT IN operator to find prodicts in PC001 that are also not in PC003 
SELECT ProductName FROM Product 
WHERE ProductCategoryID = 'PC001'
NOT IN 
(SELECT ProductName FROM Product 
WHERE ProductCategoryID = 'PC003'
);


SELECT CustomerName FROM customer c
WHERE EXISTS(
	SELECT * FROM Invoice i
    WHERE i.CustomerID = c.CustomerID);


SELECT *
FROM product
WHERE ProductName LIKE 'Toot%'
OR
ProductName LIKE 'Ele%';


SELECT ProductName,Price
FROM Product
WHERE
Price BETWEEN 100 AND 200;


SELECT Count(ProductName) AS "Product Count",CategoryName FROM Product 
JOIN Product_category ON Product.ProductCategoryID = Product_category.ProductCategoryID /* Querying Product for # of items in each Product Category*/
GROUP BY Product_category.CategoryName;

SELECT MIN(subtotal), MAX(subtotal), AVG(subtotal) AS 'Average sale'
FROM sales;

SELECT "Total Money spent", SUM(Price) AS " " FROM purchase_order;


/*================================================================================================================================================== */ 

CREATE VIEW customer_contact AS
select CustomerName, Email, PhoneNum FROM customer;

CREATE VIEW customer_recipt AS 
SELECT c.CustomerName, c.Email, i.Total, i.date FROM customer c
JOIN invoice i ON c.CustomerID = i.CustomerID;

CREATE VIEW supplier_contact AS
SELECT Supname, Contact FROM Supplier;










