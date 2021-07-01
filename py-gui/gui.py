import PySimpleGUI as sg
from helper_functions import helper_functions1


# def func(message):
#     print(message)
#
#

def gui():
    layout = [[sg.T("")],
              [sg.Image(r'/Users/colinmason/PycharmProjects/mouse-maze-vr/py-gui/f50e28dd0c102d2ccb3741b7ffcaa11a.png')],
              [sg.Text('Shapes')],
              [sg.Radio('corridor', "RADIO1", default=True, key="-corr-"), sg.Radio('ymaze', "RADIO1", key="-ymaze-"), sg.Radio('square', "RADIO1", key='-square-'), sg.Radio('circle', "RADIO1", key='-circle-'), sg.Radio('Open Field', "RADIO1", key='-of-')],
              [sg.Text('File Job')],
              [sg.Text("Choose a file: "), sg.Input(), sg.FileBrowse(key="-IN-")],
              [sg.Button("Submit File")],
              [sg.T("")],
              [sg.Text('Batch Job')],
              [sg.Text('Input Directory: '), sg.Input(), sg.FileBrowse(key='-DIR-IN-')],
              [sg.Button("Submit Batch Job")],
              [sg.T("")],
              [sg.Text('Output')],
              [sg.Text("Choose output Path:"), sg.Input(), sg.FileBrowse(key="-IN2-")],
              [sg.Cancel()]]

    window = sg.Window(title="MouseVR v1.0", layout=layout)

    # Create event loop

    while True:
        event, values = window.read()

        if event == "Submit File":
            print(values['-corr-'])
            # in_path = values["-IN-"]
            # out_path = values["-IN2-"]
            # main_df = helper_functions1.mouse_farm(in_path, 'corridor')
            # helper_functions1.sheet1_appender(out_path, main_df)

        elif event == "Cancel" or event == sg.WIN_CLOSED:
            break

    window.close()





if __name__ == "__main__":
    gui()
    print(0)





