import PySimpleGUI as sg
from helper_functions import helper_functions1


# def func(message):
#     print(message)
#
#

def gui():
    layout = [[sg.T("")],
              [sg.Text('Outputs')],
              [sg.Text("Choose output Path:"), sg.Input(), sg.FileBrowse(key="-IN2-")],
              [sg.T("")],
              [sg.Text('File Jobs')],
              [sg.Text("Choose a file: "), sg.Input(), sg.FileBrowse(key="-IN-")],
              [sg.Button("Submit File")],
              [sg.T("")],
              [sg.Text('Batch Jobs')],
              [sg.Text('Input Directory: '), sg.Input(), sg.FileBrowse(key='-DIR-IN-')],
              [sg.Button("Submit Batch Job")],
              [sg.T("")],
              [sg.Cancel()]]

    window = sg.Window(title="MouseVR v1.0", layout=layout)

    # Create event loop

    while True:
        event, values = window.read()

        if event == "Submit":
            in_path = values["-IN-"]
            out_path = values["-IN2-"]
            main_df = helper_functions1.mouse_farm(in_path, 'corridor')
            helper_functions1.sheet1_appender(out_path, main_df)

        elif event == "Cancel" or event == sg.WIN_CLOSED:
            break

    window.close()





if __name__ == "__main__":
    gui()
    print(0)





