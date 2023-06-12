import PySimpleGUI as sg
from functions import *

def Home():
    sg.theme('DarkAmber')  # Set theme

    # Define the layout
    layout = [[sg.Text('Please select an option')],
              [sg.Button('Create tables')],
              [sg.Button('Drop Table')],
              [sg.Button('Populate Tables')],
              [sg.Button('Read table')],
              [sg.Button('Search record')],
              [sg.Button('Update record')],
              [sg.Button('Delete Record')],
              [sg.Button('Exit')]]

    # Create the window
    window = sg.Window('Menu', layout)

    # Event loop
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':  # If user closes window or clicks Exit
            break
        elif event == 'Create tables':
            createTables()
            sg.popup("""TABLES: [Admin, Inventory, sales,Purchase_order,Product, Invoice,Supplier,Product_category,customer, test(for dropping)]""")
        elif event == 'Drop Table':
            drop_table(sg)
        elif event == 'Populate Tables':
            populate_table()
            sg.popup('Tables populated')
        elif event == 'Search record':
            search(sg)
        elif event == 'Update record':
            update(sg)
        elif event == 'Read table':
            view_table(sg)
        elif event == 'Delete Record':
            delete(sg)


    # Close the window
    window.close()