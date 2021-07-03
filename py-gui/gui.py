import PySimpleGUI as sg
from helper_functions import helper_functions1
# def func(message):
#     print(message)
#
#

def gui():
    layout = [
              [sg.T("")],
              [sg.Text('Shapes')],
              [sg.Radio('corridor', "RADIO1", default=True, key="-corr-"), sg.Radio('ymaze', "RADIO1", key="-ymaze-"), sg.Radio('square', "RADIO1", key='-square-'), sg.Radio('circle', "RADIO1", key='-circle-'), sg.Radio('Open Field', "RADIO1", key='-of-')],
              [sg.T("")],
              [sg.Text('File Job')],
              [sg.Text("Choose a file: "), sg.Input(), sg.FileBrowse(key="-IN-")],
              [sg.Button("Submit File")],
              [sg.T("OR")],
              [sg.Text('Batch Job')],
              [sg.Text('Choose a Directory: '), sg.Input(), sg.FileBrowse(key='-DIR-IN-')],
              [sg.Button("Submit Batch Job")],
              [sg.T("")],
              [sg.Text('Output')],
              [sg.Text("Choose output Path:"), sg.Input(), sg.FileBrowse(key="-master-"), sg.VerticalSeparator(), sg.Output(size=(40,10))],
              [sg.Cancel()]
             ]

    window = sg.Window(title="MouseVR v1.0", layout=layout)

    # Create event loop

    while True:
        event, values = window.read()

        if event == "Submit File":
            print("Executing Script...")
            window.Refresh()
            if values['-corr-']:
                shape = 'corridor'
            elif values['-ymaze-']:
                shape = 'ymaze'
            elif values['-square-']:
                shape = 'square'
            elif values['-circle-']:
                shape = 'circle'
            elif values['-of-']:
                shape = 'of'

            in_path = values["-IN-"]
            out_path = values["-master-"]
            # mouse_df = helper_functions1.mouse_farm(in_path, shape)
            # helper_functions1.sheet1_appender(out_path, mouse_df)
            print("Submitted to Output File.")
            window.Refresh()


        if event == "Submit Batch Job":
            print("Executing Script...")
            window.Refresh()
            if values['-corr-']:
                shape = 'corridor'
            elif values['-ymaze-']:
                shape = 'ymaze'
            elif values['-square-']:
                shape = 'square'
            elif values['-circle-']:
                shape = 'circle'
            elif values['-of-']:
                shape = 'of'

            in_path = values['-DIR-IN-']
            out_path = values["-IN2-"]
            mouse_df = helper_functions1.mouse_farm(in_path, shape)
            helper_functions1.sheet1_appender(out_path, mouse_df)
            sg.Popup("Running Script Execution. Please Wait.")

        elif event == "Cancel" or event == sg.WIN_CLOSED:
            break

    window.close()





if __name__ == "__main__":
    gui()
    print(0)





