import PySimpleGUI as sg
from helper_functions import file_constructors


def analysis_window():
    layout = [
        [sg.T("")],
        [sg.Text("Function1")],
        [sg.Text("Choose output Path: "), sg.Input(key='test'), sg.FileBrowse(key="-master-")]
    ]
    window = sg.Window("Analysis", layout, modal=True)
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

    window.close()


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
              [sg.Text('Choose a Directory: '), sg.Input(), sg.FolderBrowse(key='-DIR-IN-')],
              [sg.Button("Submit Batch Job")],
              [sg.T("")],
              [sg.Text('Output')],
              [sg.Text("Choose output Path:"), sg.Input('None', key='-master-', enable_events=True)],
              [sg.FileSaveAs('Make New', default_extension='.csv', target="-master-"), sg.FileBrowse('Load Existing', target='-master-')],
              [sg.Text('')],
              [sg.HorizontalSeparator()],
              [sg.Text('Console')],
              [sg.Output(size=(60,10))],
              [sg.Cancel()]
             ]
    window = sg.Window(title="MouseVR v1.0", layout=layout)

    # Create event loop

    while True:
        try:
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
                file_constructors.experiment_output(in_path, out_path, shape, gui=True, window=window)
                print('Submitted to Output File.')
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

                file_constructors.experiment_output(values['-DIR-IN-'], values["-master-"], shape, gui=True, window=window)
                print('Submitted to Output File.')
                window.Refresh()

            elif event == "Cancel" or event == sg.WIN_CLOSED:
                break

        except BaseException as error:
            print(f'An Error occurred: {error}. \nPlease check that your file paths are correct.')

    window.close()





if __name__ == "__main__":
    gui()





