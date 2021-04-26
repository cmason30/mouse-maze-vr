from colin_funcs import *

'''
Helper function for mouse_farm().
Also checks that files are not duplicated in the master sheet. 

mouse_dfpath: insert mouse_df here.
maze_array: Include maze array o behavioral file. 
master_path: Give it mastersheet file or path for new file. 

output: Will make a new csv file or append it to an existing one. Also checks for duplicate experiment input. 
'''


def sheet_appender(mouse_dfpath, maze_array, master_path, sep=',', dist_threshold=.9, copy=False):
    mouse_df = mouse_farm(mouse_dfpath, maze_array, dist_threshold)[0]
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
                    raise Exception('Warning! Filepath already found in master sheet csv. Set copy=True to append anyway.')
                else:
                    mouse_df.to_csv(master_path, mode='a', index=False, sep=sep, header=False)

            else:
                mouse_df.to_csv(master_path, mode='a', index=False, sep=sep, header=False)





def main():
    sheet_appender(r'/Users/colinmason/Desktop/ymaze_run_2_23_21 (1).behavior', 'ymaze', r'/Users/colinmason/Desktop/yorglab/rat_maze_sim/test/test4.csv')


if __name__ == "__main__":
    main()

