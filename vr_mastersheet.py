from colin_funcs import *

'''

Organizes the functions to create a dataframe with all the significant variables as columns. 

--- Inputs --- 
df_path: Give the file path of the behavioral file of interest.
maze_array: Give one of four strings( 'square', 'circle', 'ymaze', 'corridor') based on the maze that the behavior file ran on
master_path: Give the file path of the master sheet so that the new data being generated in this function appends to it. If generating
a new master sheet, then just leave as None

--- Output --- 
Outputs a dataframe with the comprehensive data from the statistical functions above.
Also outputs a dictionary with descriptive stats (right now, only outputs the time in each region for ymaze.) 
'''


def mouse_farm(df_path, maze_array, dist_threshold=.9):

    mouse_df = pd.read_csv(df_path, header=2, sep='\t')
    file_path = pd.read_csv(df_path).iloc[0, 0]
    mouse_df['filepath'] = file_path
    mouse_df['maze_type'] = maze_array
    coords = shapes(maze_array)

    '''
    Columns of dataframe up to this point:
    ['#Snapshot Timestamp', 'Trigger Region Identifier', 'Position.X',
       'Position.Y', 'Position.Z', 'Forward.X', 'Forward.Y', 'Forward.Z',
       'filepath', 'maze_type']
    '''

    if maze_array == 'ymaze':
        '''
        Appends the ymaze region information to the dataframe.
        New Columns appended: ['time_diff', 'region']
        time_diff = Difference between timestamp of n row and n-1 row
        gets row region that the coordinates were found in. (Returns as string of 'top', 'center', 'left', 'right')

        Also creates des_df which is the one row dataframe information.
        keys in des_df: ['file_path', 'center_time', 'top_time', 'left_time', 'right_time']
        
        '''
        time_spent = y_maze_time_spent(mouse_df)

        mouse_df = pd.concat([mouse_df, time_spent[1]], axis=1)

        des_df = {'file_path': file_path}
        des_df.update(time_spent[0])

        '''
        # Next, finish off with mouse edge distance function which adds two more columns:
        # Columns: ['mouse_dist', 'distance_marked']
        '''
        # TODO: need path of master dataframe of descriptive stats (2nd dataframe, in case we want to append that data as well.)

        dist_df = mouse_edge_distance(mouse_df, coords, dist_threshold)

        mouse_df = pd.concat([mouse_df, dist_df], axis=1)

        return mouse_df, des_df

    else:
        mouse_df['time_diff'] = mouse_df['#Snapshot Timestamp'].diff()
        mouse_df['region'] = np.nan
        empty_dict = 'nothing here'
        mouse_df = mouse_edge_distance(mouse_df, coords)
        return mouse_df, empty_dict


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

