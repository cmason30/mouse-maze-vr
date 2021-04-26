import os
import pandas as pd
import colin_sub_funcs
from shapely.geometry import Point
import numpy as np

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

def mouse_edge_distance(behavioral_df, maze_coordinates, distance_threshold=.1):
    df_test = behavioral_df.copy()

    # Gets inner shape to make distance threshold boundary polygons
    polygon_maze, reduced_poly = colin_sub_funcs.shape_shrink(maze_coordinates, distance_threshold)

    # Checks coordinates in each row and returns the mouses distance from the edge and True or False if mouse is
    # within the threshold distance to the wall
    df_test["mouse_dist"] = df_test.apply(lambda row: polygon_maze.exterior.distance(Point(row["Position.X"], row["Position.Y"])), axis=1)
    df_test['distance_marked'] = df_test.apply(lambda row: 1 if reduced_poly.contains(Point(row["Position.X"], row["Position.Y"])) else 0, axis=1)

    # Checks that all coordinates are in Polygon
    colin_sub_funcs.within_bounds(df_test, polygon_maze)

    # outputs two columns: mouse_dist, distance_marked
    return df_test[['mouse_dist', 'distance_marked']]



'''
y_maze_time_spent()
Gets a dictionary of time spent in each region along with [[time_diff, region]] master sheet columns

Input

behavioral_df: the mouse behavioral dataframe

Output

time_spent dictionary, columns of time_diff and region
'''

def y_maze_time_spent(behavioral_df):
    ymaze_mouse = behavioral_df.copy()
    time_spent_region = {}
    ymaze_mouse['time_diff'] = ymaze_mouse['#Snapshot Timestamp'].diff()


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

    # New output df with the labelled columns

    out_df = ymaze_mouse.drop(columns=['top', 'center', 'left', 'right'])

    # Set new key names to output dictionary
    new_names = {'center': 'center_time', 'left': 'left_time', 'right': 'right_time', 'top': 'top_time'}
    time_spent_region = dict((new_names[key], value) for (key, value) in time_spent_region.items())

    return time_spent_region, out_df[['time_diff', 'region']]


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








def main():
    df_test_ymaze = pd.read_csv(r'/Users/colinmason/Desktop/ymaze_run_2_23_21 (1).behavior', header=2, sep='\t')
    # coords = np.array([[-433.013, -452.582],
    #                    [0, -202.582],
    #                    [433.013, -452.582],
    #                    [558.013, -236.075],
    #                    [125, 13.925],
    #                    [125, 513.924],
    #                    [-125, 513.924],
    #                    [-125, 13.925],
    #                    [-558.013, -236.075]])
    #
    print(y_maze_time_spent(df_test_ymaze)[0])
    # print(df_test_ymaze['#Snapshot Timestamp'][0] + y_maze_time_spent(df_test_ymaze)[1]['time_diff'].sum())
    # time = 180.017000

if __name__ == "__main__":
    main()





