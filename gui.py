import PySimpleGUI as sg
import mysql.connector
from functions import *
import re



def Home():
    sg.theme('DarkAmber')
    layout = [
        [sg.Text('POS System Dashboard', size=(30, 1), justification='center', font=("Helvetica", 25))],
        [sg.Button('Make a Sale', size=(20, 2)), sg.Button('View Inventory', size=(20, 2))],
       # [sg.Button('Generate Report', size=(20, 2)), sg.Button('Exit', size=(20, 2))]
    ]

    window = sg.Window('POS System', layout, size=(500, 300))
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == 'Make a Sale':
            process_sale()
        elif event == 'View Inventory':
            view_inventory()
        #elif event == 'Generate Report':
            #generate_report()

    window.close()

def initialize_database(cursor):
    try:
        createTables()
        populate_table()
    except mysql.connector.Error as err:
        print(f"Error occurred: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")

def extract_product_id_and_quantity(item):
    # Assuming item format is 'Product: <product_id>, Quantity: <quantity>, Cost: $<cost>'
    parts = item.split(', ')
    product_id = parts[0].split(': ')[1]
    quantity = int(parts[1].split(': ')[1])
    return product_id, quantity

def fetch_products():
    cursor.execute("SELECT ProductCategoryID, CategoryName FROM Product_category")
    categories = cursor.fetchall()

    category_products = {}
    all_product_ids = set()  # Set to store all product IDs
    for cat_id, cat_name in categories:
        cursor.execute("""
            SELECT p.ProductID, p.ProductName, i.Quantity, p.Price  # Assuming Price is in Product table
            FROM Product p 
            JOIN Inventory i ON p.inventoryID = i.inventoryID 
            WHERE ProductCategoryID = %s""", (cat_id,))
        products = cursor.fetchall()
        category_products[cat_name] = products
        all_product_ids.update(pid for pid, _, _, _ in products)

    return category_products, all_product_ids


def process_sale():
    sg.theme('DarkAmber')
    products_by_category, valid_product_ids = fetch_products()  # Fetch valid product IDs too
    product_dropdowns = []
    product_details = {}  # Dictionary to store product details including price
    for category, products in products_by_category.items():
        for pid, pname, stock, price in products:
            product_details[pid] = {"name": pname, "stock": stock, "price": price}
        dropdown = sg.Combo([f"{pid} - {pname} [Stock: {stock}]" for pid, pname, stock, _ in products], key=f'dd_{category}')
        product_dropdowns.append([sg.Text(category), dropdown])

    layout = [
        [sg.Text('Product ID'), sg.InputText(key='product_id')],
        [sg.Text('Quantity'), sg.InputText(key='quantity')],
        [sg.Button('Add to Cart'), sg.Button('Remove from Cart'), sg.Button('Finalize Sale')],
        product_dropdowns,
        [sg.Listbox(values=[], size=(40, 10), key='cart')],
        [sg.Text('Total: $0', key='total')],
    ]

    window = sg.Window('Process Sale', layout)

    cart_items = []
    total_cost = 0

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        # Update Product ID field when product is selected from dropdown
        if event.startswith('dd_'):
            selected_product = values[event].split(' - ')[0] if values[event] else ''
            window['product_id'].update(selected_product)

        if event == 'Add to Cart':
            product_id = values['product_id']
            quantity = values['quantity']

            # Validate product ID
            if product_id not in valid_product_ids:
                sg.popup('Error: Invalid Product ID')
                continue

            # Error handling for missing quantity
            if not quantity:
                sg.popup('Error: No quantity specified')
                continue

            quantity = int(quantity)
            price = product_details[product_id]["price"]
            cost = price * quantity

            cart_items.append(f'Product: {product_id}, Quantity: {quantity}, Cost: ${cost}')
            total_cost += cost

            window['cart'].update(cart_items)
            window['total'].update(f'Total: ${total_cost}')

        if event == 'Remove from Cart':
            if not window['cart'].get():
                sg.popup("No item selected to remove")
                continue

            try:
                selected_item = values['cart'][0]
                cart_items.remove(selected_item)
                total_cost -= extract_cost_from_cart_item(selected_item)
                window['cart'].update(cart_items)
                window['total'].update(f'Total: ${total_cost}')
            except Exception as e:
                sg.popup(f"Error removing item: {e}")

        if event == 'Finalize Sale':
            if not cart_items:
                sg.popup('Error: No items in the cart')
                continue

            for item in cart_items:
                product_id, quantity_sold = extract_product_id_and_quantity(item)
                print(item)
                print(product_id)
                print(quantity_sold)
                update_inventory(product_id, quantity_sold)

            sg.popup(f'Sale finalized.\nTotal Cost: ${total_cost}')
            break

    window.close()

def extract_cost_from_cart_item(item):
    cost_str = item.split('Cost: $')[1]
    return float(cost_str)

def extract_product_id_and_quantity(item):
    parts = item.split(', ')
    product_id = parts[0].split(': ')[1]
    quantity = int(parts[1].split(': ')[1])
    return product_id, quantity


def update_inventory(product_id, quantity_sold):
    # Find the inventoryID associated with the ProductID
    cursor.execute("SELECT inventoryID FROM Product WHERE ProductID = %s", (product_id,))
    result = cursor.fetchone()

    if result is None:
        sg.popup(f"No product record found for Product ID: {product_id}")
        return

    inventory_id = result[0]

    # Fetch current inventory level using inventoryID
    cursor.execute("SELECT Quantity FROM Inventory WHERE inventoryID = %s", (inventory_id,))
    result = cursor.fetchone()

    if result is None:
        sg.popup(f"No inventory record found for Inventory ID: {inventory_id}")
        return

    current_quantity = result[0]

    # Check if enough stock is available
    if current_quantity < quantity_sold:
        sg.popup(f"Not enough stock for Product ID: {product_id}. Current stock: {current_quantity}")
        return

    # Calculate new inventory level
    new_quantity = current_quantity - quantity_sold

    # Update inventory in database using inventoryID
    cursor.execute("UPDATE Inventory SET Quantity = %s WHERE inventoryID = %s", (new_quantity, inventory_id,))
    mydb.commit()

def fetch_inventory_data():
    cursor.execute("""
        SELECT p.ProductID, p.ProductName, i.Quantity, p.Price 
        FROM Product p
        JOIN Inventory i ON p.inventoryID = i.inventoryID
    """)
    return cursor.fetchall()

def view_inventory():
    # Fetch inventory data
    cursor.execute("""
        SELECT p.ProductID, p.ProductName, i.Quantity, p.Price 
        FROM Product p
        JOIN Inventory i ON p.inventoryID = i.inventoryID
    """)
    inventory_data = cursor.fetchall()

    # Convert data to list of lists
    inventory_data = [list(row) for row in inventory_data]

    # Define the window layout
    layout = [
        [sg.Text('Inventory', font=('Helvetica', 16))],
        [sg.Table(values=inventory_data, headings=['Product ID', 'Product Name', 'Quantity', 'Price'], 
                  display_row_numbers=True, auto_size_columns=True, key='-TABLE-', 
                  num_rows=min(25, len(inventory_data)))],
        [sg.Button('Update Product'), sg.Button('Add New Product'), sg.Button('Exit')]
    ]

    # Create the window
    window = sg.Window('View Inventory', layout)

    # Event loop
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == 'Update Product':
            selected_row = values['-TABLE-']
            if selected_row:
                selected_product = inventory_data[selected_row[0]]
                update_product(selected_product)
            else:
                sg.popup("Please select a product to update")
        elif event == 'Add New Product':
            add_new_product()

    window.close()



def update_product(selected_product):
    layout = [
        [sg.Text('Product ID'), sg.InputText(selected_product[0], key='product_id', disabled=True)],
        [sg.Text('Quantity'), sg.InputText(key='quantity', default_text=selected_product[2])],
        [sg.Text('Price'), sg.InputText(key='price', default_text=selected_product[3])],
        [sg.Button('Submit'), sg.Button('Cancel')]
    ]

    window = sg.Window('Update Product', layout)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        elif event == 'Submit':
            quantity = values['quantity']
            price = values['price']
            product_id = selected_product[0]

            if not quantity.isdigit() or int(quantity) < 0:
                sg.popup("Invalid quantity. Please enter a non-negative number.")
                continue
            if not price.isdigit() or int(price) < 0:
                sg.popup("Invalid price. Please enter a non-negative number.")
                continue

            # Update database logic
            cursor.execute("""
                UPDATE Product 
                SET Price = %s
                WHERE ProductID = %s
            """, (int(price), product_id,))
            cursor.execute("""
                UPDATE Inventory 
                SET Quantity = %s
                WHERE inventoryID = (
                    SELECT inventoryID FROM Product WHERE ProductID = %s
                )
            """, (int(quantity), product_id,))
            mydb.commit()

            sg.popup('Product updated successfully!')
            break
            
    window.close()
    
    



def add_new_product():
    # Fetch product categories
    cursor.execute("SELECT ProductCategoryID, CategoryName FROM Product_category")
    categories = cursor.fetchall()

    # Prepare category dropdown with both ID and name
    category_combo = [f"{cat[0]} - {cat[1]}" for cat in categories]

    layout = [
        [sg.Text('Product ID'), sg.InputText(key='product_id')],
        [sg.Text('Product Name'), sg.InputText(key='product_name')],
        [sg.Text('Quantity'), sg.InputText(key='quantity')],
        [sg.Text('Price'), sg.InputText(key='price')],
        [sg.Text('Product Category'), sg.Combo(category_combo, key='product_category')],
        [sg.Text('Inventory ID'), sg.InputText(key='inventory_id')],
        [sg.Button('Submit'), sg.Button('Cancel')]
    ]

    window = sg.Window('Add New Product', layout)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        elif event == 'Submit':
            product_id = values['product_id']
            product_name = values['product_name']
            quantity = values['quantity']
            price = values['price']
            product_category_id = values['product_category'].split(' - ')[0]  # Extract ID from selection
            inventory_id = values['inventory_id']

            if not re.match(r'PR\d{3}', product_id):
                sg.popup("Invalid Product ID. It must match PR###.")
                continue
            if not re.match(r'INV\d{2}', inventory_id):
                sg.popup("Invalid Inventory ID. It must match INV##.")
                continue
            if not quantity.isdigit() or int(quantity) < 0:
                sg.popup("Invalid quantity. Please enter a non-negative number.")
                continue
            if not price.isdigit() or int(price) < 0:
                sg.popup("Invalid price. Please enter a non-negative number.")
                continue

            # Check for duplicate product name
            cursor.execute("SELECT COUNT(*) FROM Product WHERE ProductName = %s", (product_name,))
            if cursor.fetchone()[0] > 0:
                sg.popup("A product with this name already exists. Please use a different name.")
                continue

            # Add product to database
            cursor.execute("""
                INSERT INTO Inventory (inventoryID, Quantity)
                VALUES (%s, %s)
            """, (inventory_id, int(quantity)))
            cursor.execute("""
                INSERT INTO Product (ProductID, ProductName, Price, ProductCategoryID, inventoryID)
                VALUES (%s, %s, %s, %s, %s)
            """, (product_id, product_name, int(price), product_category_id, inventory_id))
            mydb.commit()

            sg.popup('New product added successfully!')
            break
    
    window.close()
   
    




#def generate_report():
    # Function to generate/view reports
    #pass

if __name__ == "__main__":
    # Database connection
    mydb = mysql.connector.connect(
        host="sql5.freesqldatabase.com",
        port =3306,
        user="sql5675113",
        password="X4YdRtGYWm",
        database="sql5675113"
    )
    cursor = mydb.cursor()

    initialize_database(cursor)
    Home()
