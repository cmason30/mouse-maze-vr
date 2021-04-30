from vr_vis import mouse_path, time_regon_plot_ymaze
from mastersheet_mod_funcs import sheet1_appender
from colin_funcs import mouse_farm
import pandas as pd
import os

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
def experiment_output(directory, master_path1, maze_array, dist_threshold=.1):

    for behavioral_file in file_walk(directory):
        mouse_df = mouse_farm(behavioral_file, maze_array, dist_threshold)
        sheet1_appender(mouse_df[0], master_path1)
        desc_sheet2 = master_path1[:len(master_path1) - 4] + '_sheet2' + '.csv'
        sheet1_appender(mouse_df[1], desc_sheet2)
        print('File Input')


def main():

    directory = r'/Users/colinmason/Desktop/yorglab/rat_maze_sim/CPP Experiment Data/Day 4'
    master_file = r'/Users/colinmason/Desktop/yorglab/rat_maze_sim/test/vr_master_v1.csv'
    # file_path = r'/Users/colinmason/Desktop/yorglab/CPP Experiment Data/Day 1/8002_CPP_cocaine_blue_maze.behavior'
    # test_df = pd.read_csv(r'/Users/colinmason/Desktop/yorglab/CPP Experiment Data/Day 1/8002_CPP_cocaine_blue_maze.behavior', header=2, sep='\t')
    # file_line = pd.read_csv(file_path).iloc[0, 0]
    # print(file_line)

    experiment_output(directory,master_file, 'corridor')


if __name__ == '__main__':
    main()


# TODO: Incorporate database function for uploading mastersheet?
# TODO: Automate the process of reading the maze type in the behavioral files so that they will not need to be input manuall