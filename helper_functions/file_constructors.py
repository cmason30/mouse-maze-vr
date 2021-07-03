import os
import pandas as pd
from helper_functions import helper_functions1

'''
Gets all file paths in a given directory 

Input
directory: Any folder to get files inside

Output
An iterator object of all the file paths contained within. 
'''
def file_walk(directory):
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))

'''
Helper function for mouse_farm(). Sends data to CSV. 

Also checks that files are not duplicated in the master sheet. 

mouse_dfpath: insert mouse_df here.
maze_array: Include maze array o behavioral file. 
master_path: Give it mastersheet file or path for new file. 

output: Will make a new csv file or append it to an existing one. Also checks for duplicate experiment input. 
'''


def sheet1_appender(mouse_df, master_path, sep=',', copy=False):
    if not os.path.isfile(master_path):
        mouse_df.to_csv(master_path, mode='a', index=False, sep=sep)
    else:
        if len(mouse_df.columns) != len(pd.read_csv(master_path, nrows=1, sep=sep).columns):
            raise Exception("Columns do not match!! Dataframe has " + str(len(mouse_df.columns)) + " columns. CSV file has " + str(len(pd.read_csv(master_path, nrows=1, sep=sep).columns)) + " columns.")
        elif not (mouse_df.columns == pd.read_csv(master_path, nrows=1, sep=sep).columns).all():
            raise Exception("Columns and column order of dataframe and csv file do not match!!")
        else:
            master = pd.read_csv(master_path)
            if not copy:
                if mouse_df['filepath'].unique()[0] in master['filepath'].unique():
                    return print(f'Warning! Filepath[{mouse_df["filepath"].unique()[0]}] is already found in master sheet csv. Set copy=True to append anyway.')
                else:
                    mouse_df.to_csv(master_path, mode='a', index=False, sep=sep, header=False)

            else:
                mouse_df.to_csv(master_path, mode='a', index=False, sep=sep, header=False)


# ---------Final Output Functions --------------- #



'''
Loops through all experiment files in a given directory and returns them as an organized CSV. 

Input
    directory: Given folder of behavioral files to read in.
    master_path1: Desired mastersheet to input files to. Or input a new file name at end of file_path string and it will create a new masterhseet
    maze_array: Give maze type
    dist_threshold: For distance from wall function

Output
    1. Appends to or makes a new master sheet csv
    2. Makes another csv of ymaze region time spent values. Or appends to an existing one.
        This second csv will have the same name as the master sheet, but with *_sheet.csv at the end. 
'''


def experiment_output(dir_or_file, master_path1, maze_array, dist_threshold=.1, gui=False, window=None):

    if os.path.isdir(dir_or_file):
        count = 0
        for _ in file_walk(dir_or_file):
            count += 1

        for idx, behavioral_file in enumerate(file_walk(dir_or_file)):
            mouse_df = helper_functions1.mouse_farm(behavioral_file, maze_array, dist_threshold)
            sheet1_appender(mouse_df[0], master_path1)
            desc_sheet2 = master_path1[:len(master_path1) - 4] + '_sheet2' + '.csv'
            sheet1_appender(mouse_df[1], desc_sheet2)
            print(f'File Input {idx} of {count}.')
            if gui:
                window.Refresh()

    elif os.path.isfile(dir_or_file):
        mouse_df = helper_functions1.mouse_farm(dir_or_file, maze_array, dist_threshold)
        sheet1_appender(mouse_df[0], master_path1)
        desc_sheet2 = master_path1[:len(master_path1) - 4] + '_sheet2' + '.csv'
        sheet1_appender(mouse_df[1], desc_sheet2)
        print('File Input.')
        if gui:
            window.Refresh()

    else:
        print('Please insert correct file or directory.')
        if gui:
            window.Refresh()




def main():
    experiment_output(r'/Users/colinmason/Desktop/yorglab/rat_maze_sim/CPP Experiment Data/Day 1', r'/Users/colinmason/Desktop/yorglab/rat_maze_sim/test/vr_master_v2.csv', 'corridor')
    experiment_output(r'/Users/colinmason/Desktop/yorglab/rat_maze_sim/CPP Experiment Data/Day 2', r'/Users/colinmason/Desktop/yorglab/rat_maze_sim/test/vr_master_v2.csv', 'corridor')
    experiment_output(r'/Users/colinmason/Desktop/yorglab/rat_maze_sim/CPP Experiment Data/Day 3', r'/Users/colinmason/Desktop/yorglab/rat_maze_sim/test/vr_master_v2.csv', 'corridor')
    experiment_output(r'/Users/colinmason/Desktop/yorglab/rat_maze_sim/CPP Experiment Data/Day 4', r'/Users/colinmason/Desktop/yorglab/rat_maze_sim/test/vr_master_v2.csv', 'corridor')
    experiment_output(r'/Users/colinmason/Desktop/yorglab/rat_maze_sim/CPP Experiment Data/Day 5', r'/Users/colinmason/Desktop/yorglab/rat_maze_sim/test/vr_master_v2.csv', 'corridor')
    experiment_output(r'/Users/colinmason/Desktop/yorglab/rat_maze_sim/CPP Experiment Data/Day 6', r'/Users/colinmason/Desktop/yorglab/rat_maze_sim/test/vr_master_v2.csv', 'corridor')
    experiment_output(r'/Users/colinmason/Desktop/yorglab/rat_maze_sim/CPP Experiment Data/Final Test Day', r'/Users/colinmason/Desktop/yorglab/rat_maze_sim/test/vr_master_v2.csv', 'ymaze')




if __name__ == "__main__":

    main()