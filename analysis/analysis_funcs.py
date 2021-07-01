import pandas as pd
import numpy as np

# for path, df in df_m[df_m['maze_type'] == maze].groupby('filepath'):

def overall_time(mouse_df, units):
    mouse_df['distance_marked'] = np.where(mouse_df['mouse_from_wall_units'] < 34 + units, 1, 0)
    sum = mouse_df[mouse_df['distance_marked'] == 1]['time_diff'].sum()
    wall_percent = sum / 900

    wall_dict = {'sum': sum, '%_near_wall': wall_percent, 'units': units}

    # final_df = pd.DataFrame([[end_list['Time wall'].mean(), end_list['% wall'].mean(), end_list['% wall'].max(),
    #                           end_list['% wall'].min(), units]],
    #                         columns=['Overall Avg. Time(sec)', 'Avg. Overall %', 'Max%', 'Min%', 'Within # units'])
    return wall_dict

