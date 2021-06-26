import helper_functions1
import helper_functions2
import pandas as pd
import os

# ---------------------------------------- Master sheet generator ------------------------------------------------ #


'''

Organizes the functions to create a dataframe with all the significant variables as columns. 

Input
df_path: Give the file path of the behavioral file of interest.
maze_array: Give one of four strings( 'square', 'circle', 'ymaze', 'corridor') based on the maze that the behavior file ran on
master_path: Give the file path of the master sheet so that the new data being generated in this function appends to it. If generating
a new master sheet, then just leave as None

Output
Outputs a dataframe with the comprehensive data from the statistical functions above.
Also outputs a second dataframe with descriptive stats gives region times and speed/velocity 
'''


def mouse_farm(df_path, maze_array, dist_threshold=.1):
    mouse_df = pd.read_csv(df_path, header=2, sep='\t')
    # file_path = pd.read_csv(df_path).iloc[0, 0]
    file_name = df_path

    mouse_df['filepath'] = df_path
    mouse_df['maze_type'] = maze_array

    mouse_distance = helper_functions1.mouse_edge_distance(mouse_df, maze_array, dist_threshold)
    mouse_df['speed'] = helper_functions2.calc_speed(mouse_df)

    time_spent = helper_functions1.y_maze_time_spent(mouse_df, file_name, maze_array)

    final_df = pd.concat([mouse_df, mouse_distance, time_spent[1]], axis=1)
    des_dict = pd.concat([time_spent[0], helper_functions2.avg_velocity(mouse_df)], axis=1)

    return final_df, des_dict



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


def experiment_output(directory, master_path1, maze_array, dist_threshold=.1):
    for behavioral_file in helper_functions1.file_walk(directory):
        mouse_df = mouse_farm(behavioral_file, maze_array, dist_threshold)
        sheet1_appender(mouse_df[0], master_path1)
        desc_sheet2 = master_path1[:len(master_path1) - 4] + '_sheet2' + '.csv'
        sheet1_appender(mouse_df[1], desc_sheet2)
        print('File Input')



def main():
    experiment_output(r'/Users/colinmason/Desktop/yorglab/rat_maze_sim/CPP Experiment Data/Day 1',
                      r'/Users/colinmason/Desktop/yorglab/rat_maze_sim/test/test_file10.csv',
                      'corridor')


if __name__ == "__main__":
    main()

