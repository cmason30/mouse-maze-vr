import os
import pandas as pd
import colin_sub_funcs
from shapely.geometry import Point
import numpy as np
from noah_funcs import avgVelocity, calcSpeed

'''
mouse_edge_distance()
Detects when mouse is near boundaries of maze.

Input
behavioral_df: Behavioral data as panddas dataframe
maze_coordinates: String label of maze. Options include: [square, OF, corridor, ymaze, circle]
distance_threshold: The percent distance from wall of mouse. Must be between 0 and 1

Output
Dataframe of two columns:
    mouse_dist - unit distance from wall for each coordinate
    distance_marked - marks coordinates with 1 if mouse is within distance threshold that was set
'''

def mouse_edge_distance(behavioral_df, maze_coordinates, distance_threshold):
    df_test = behavioral_df.copy()

    # Gets inner shape to make distance threshold boundary polygons
    polygon_maze, reduced_poly = colin_sub_funcs.shape_shrink(maze_coordinates, distance_threshold)

    # Checks coordinates in each row and returns the mouses distance from the edge and True or False if mouse is
    # within the threshold distance to the wall
    df_test["mouse_from_wall_units"] = df_test.apply(lambda row: polygon_maze.exterior.distance(Point(row["Position.X"], row["Position.Y"])), axis=1)
    df_test['distance_marked'] = df_test.apply(lambda row: 1 if reduced_poly.contains(Point(row["Position.X"], row["Position.Y"])) else 0, axis=1)
    df_test['mouse_from_wall_%_input'] = distance_threshold

    # Checks that all coordinates are in Polygon
    colin_sub_funcs.within_bounds(df_test, polygon_maze)

    # outputs two columns: mouse_dist, distance_marked
    return df_test[["mouse_from_wall_units", 'distance_marked', 'mouse_from_wall_%_input']]



'''
y_maze_time_spent()
Gets a dictionary of time spent in each region along with [[time_diff, region]] master sheet columns

Input

behavioral_df: the mouse behavioral dataframe

Output

time_spent dictionary, columns of time_diff and region
'''

def y_maze_time_spent(behavioral_df, file_name, maze_type, speed):
    ymaze_mouse = behavioral_df.copy()
    ymaze_mouse['time_diff'] = ymaze_mouse['#Snapshot Timestamp'].diff()
    if maze_type == 'ymaze':
        time_spent_region = {}

    # Labels the different regions in a dictionary
        regions_coordinates = colin_sub_funcs.regions_dictionary()

    # Uses the key value pairs of regions_dict to label which region each coordinate resides
    # Lastly sums up the time spent in each region as a second dictionary

        for key, value in regions_coordinates.items():

            ymaze_mouse[key] = ymaze_mouse.apply(lambda row: value.contains(Point(row["Position.X"], row["Position.Y"])),axis=1)
            time_spent_region[key] = ymaze_mouse[ymaze_mouse[key] == True]['time_diff'].sum()

    # Applies the region_match function to each row and gives a string label for where the coordinate was found
        ymaze_mouse['region'] = ymaze_mouse.apply(colin_sub_funcs.region_match, axis=1)
        first_time = ymaze_mouse['#Snapshot Timestamp'][0]
        first_region = ymaze_mouse['region'][0]
        time_spent_region[first_region] += first_time

    # Set new key names to output dictionary
        new_names = {'center': 'center_time', 'left': 'left_time', 'right': 'right_time', 'top': 'top_time'}
        time_spent_region = dict((new_names[key], value) for (key, value) in time_spent_region.items())

        extra_vals = {'filepath': file_name, 'avg_vel': avgVelocity(behavioral_df), 'avg_speed': speed}
        time_spent_region.update(extra_vals)

    else:
        time_spent_region = {
                'filepath': file_name,
                'top_time': np.nan,
                'center_time': np.nan,
                'left_time': np.nan,
                'right_time': np.nan,
                'avg_vel': avgVelocity(behavioral_df),
                'avg_speed': speed
                }
        ymaze_mouse['region'] = np.nan

    des_df = pd.DataFrame(time_spent_region, columns=['filepath','top_time','center_time','left_time','right_time','avg_vel','avg_speed'], index=[0])

    return des_df, ymaze_mouse[['time_diff', 'region']]


'''
Organizes maze coordinates for function use. 
'''

def shapes(maze_array):
    if (maze_array.lower() == 'square') or (maze_array.lower() == 'of'):
        coords = np.array([[750, -750],
                           [-750, -750],
                           [-750, 750],
                           [750, 750]])

    elif maze_array.lower() == 'circle':
        coords = 750  # <- radius

    elif maze_array.lower() == 'ymaze':
        coords = np.array([[-433.013, -452.582],
                           [0, -202.582],
                           [433.013, -452.582],
                           [558.013, -236.075],
                           [125, 13.925],
                           [125, 513.924],
                           [-125, 513.924],
                           [-125, 13.925],
                           [-558.013, -236.075]])

    elif maze_array.lower() == 'corridor':
        coords = np.array([[-75, -1332.286],
                           [-75, 1332.286],
                           [75, 1332.286],
                           [75, -1332.286]])

    else:
        return print('Give a valid shape type.')

    return coords


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

    coords = shapes(maze_array)

    mouse_df['filepath'] = df_path
    mouse_df['maze_type'] = maze_array

    mouse_distance = mouse_edge_distance(mouse_df, coords, dist_threshold)
    mouse_speed = calcSpeed(mouse_df)
    time_spent = y_maze_time_spent(mouse_df, file_name, maze_array, mouse_speed[1])

    final_df = pd.concat([mouse_df, mouse_distance, mouse_speed[0], time_spent[1]], axis=1)
    des_dict = time_spent[0]

    return final_df, des_dict



def main():
    print(mouse_farm(r'/Users/colinmason/Desktop/yorglab/rat_maze_sim/CPP Experiment Data/Day 1/8003_CPP_cocaine_white _maze.behavior', 'corridor')[1])

if __name__ == "__main__":
    main()





