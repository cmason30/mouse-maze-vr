import PySimpleGUI as sg
from helper_functions import file_constructors
from helper_functions import helper_functions1
import pandas as pd

# def analysis_window():
#     try:
#         # Header=None means you directly pass the columns names to the dataframe
#         df = pd.read_csv(filename, sep=',', engine='python', header=None)
#         data = df.values.tolist()  # read everything else into a list of rows
#         if button == 'Yes':  # Press if you named your columns in the csv
#             # Uses the first row (which should be column names) as columns names
#             header_list = df.iloc[0].tolist()
#             # Drops the first row in the table (otherwise the header names and the first row will be the same)
#             data = df[1:].values.tolist()
#         elif button == 'No':  # Press if you didn't name the columns in the csv
#             # Creates columns names for each column ('column0', 'column1', etc)
#             header_list = ['column' + str(x) for x in range(len(data[0]))]
#     except:
#         sg.popup_error('Error reading file')
#         return
#
#     layout = [
#         [sg.T("")],
#
#         [sg.Text("Function1")],
#         [sg.Text("Choose output Path: "), sg.Input(key='test'), sg.FileBrowse(key="-master-")]
#     ]
#     window = sg.Window("Analysis", layout, modal=True)
#     while True:
#         event, values = window.read()
#         if event == "Exit" or event == sg.WIN_CLOSED:
#             break
#
#     window.close()


def gui():
    layout = [

              [sg.T("")],
              [sg.Frame('Shapes',
              [
                [sg.Radio('Corridor', "RADIO1", default=True, key="-corr-"), sg.Radio('YMaze', "RADIO1", key="-ymaze-"), sg.Radio('Square', "RADIO1", key='-square-'), sg.Radio('Circle', "RADIO1", key='-circle-'), sg.Radio('Open Field', "RADIO1", key='-of-')],
                [sg.T("")]])],

              [sg.T('')],
              [sg.Frame('File Job',
              [
                [sg.Text("Choose a file: "), sg.Input(), sg.FileBrowse(key="-IN-")],
                [sg.Button("Submit File")],
                # [sg.T("OR")],
                # [sg.Text('Batch Job')],
                # [sg.Text('Choose a Directory: '), sg.Input(), sg.FolderBrowse(key='-DIR-IN-')],
                # [sg.Button("Submit Batch Job")],
                [sg.T('')]
              ])],

              [sg.T("")],
              # [sg.Frame('Output',
              # [
              #     [sg.T("")],
              #     [sg.Text("Choose output Path:"), sg.Input('None', key='-master-', enable_events=True)],
              #     [sg.FileSaveAs('Make New', default_extension='.csv', target="-master-"), sg.FileBrowse('Load Existing', target='-master-')],
              #     [sg.Text('')]
              # ])],

              [sg.T('')],
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
                # out_path = values["-master-"]
                # file_constructors.experiment_output(in_path, out_path, shape, gui=True, window=window)
                helper_functions1.generate_analyis(behavioral_filepath=in_path, maze_array=shape, dist_threshold=.1)
                print('File Processed.')
                window.Refresh()



            # if event == "Submit Batch Job":
            #     print("Executing Script...")
            #     window.Refresh()
            #     if values['-corr-']:
            #         shape = 'corridor'
            #     elif values['-ymaze-']:
            #         shape = 'ymaze'
            #     elif values['-square-']:
            #         shape = 'square'
            #     elif values['-circle-']:
            #         shape = 'circle'
            #     elif values['-of-']:
            #         shape = 'of'
            #
            #     file_constructors.experiment_output(values['-DIR-IN-'], values["-master-"], shape, gui=True, window=window)
            #     print('Submitted to Output File.')
            #     window.Refresh()

            elif event == "Cancel" or event == sg.WIN_CLOSED:
                break

        except BaseException as error:
            print(f'An Error occurred: {error}. \nPlease check that your file paths are correct.')

    window.close()





if __name__ == "__main__":
    gui()





