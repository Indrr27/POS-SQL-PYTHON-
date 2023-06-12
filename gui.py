import PySimpleGUI as sg
from Home import Home

def login():
    sg.theme('DarkAmber')
    layout = [[sg.Text('Please enter your login credentials')],
              [sg.Text('Username'), sg.InputText()],
              [sg.Text('Password'), sg.InputText(password_char='*')],
              [sg.Button('Login'), sg.Button('Close')]]

    window = sg.Window('Login', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Close':
            break
        elif values[0] == 'admin' and values[1] == 'admin':
            window.close()
            Home()
            break
        else:
            sg.popup('Incorrect login credentials.')
login()