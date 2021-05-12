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

def mouse_edge_distance(behavioral_df, maze_name, distance_threshold):
    df_test = behavioral_df.copy()
    shape = colin_sub_funcs.shapes(maze_name)

    # Gets inner shape to make distance threshold boundary polygons
    polygon_maze, reduced_poly = colin_sub_funcs.shape_shrink(shape, distance_threshold)

    # Checks coordinates in each row and returns the mouses distance from the edge and True or False if mouse is
    # within the threshold distance to the wall
    df_test["dist_wall_units"] = df_test.apply(lambda row: polygon_maze.exterior.distance(Point(row["Position.X"], row["Position.Y"])) - 33.9, axis=1)
    df_test['distance_marked'] = df_test.apply(lambda row: 1 if reduced_poly.contains(Point(row["Position.X"], row["Position.Y"])) else 0, axis=1)

    # Checks that all coordinates are in Polygon
    colin_sub_funcs.within_bounds(df_test, polygon_maze)

    # outputs two columns: mouse_dist, distance_marked
    return df_test[["dist_wall_units", 'distance_marked']]



'''
y_maze_time_spent()
Gets a dictionary of time spent in each region along with [[time_diff, region]] master sheet columns

Input

behavioral_df: the mouse behavioral dataframe

Output

time_spent dictionary, columns of time_diff and region
'''

def y_maze_time_spent(behavioral_df, file_name, maze_type):
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

        extra_vals = {'filepath': file_name, 'maze_type': maze_type}
        time_spent_region.update(extra_vals)

    else:
        time_spent_region = {
                'filepath': file_name,
                'top_time': np.nan,
                'center_time': np.nan,
                'left_time': np.nan,
                'right_time': np.nan,
                'maze_type': maze_type
                }
        ymaze_mouse['region'] = np.nan

    des_df = pd.DataFrame(time_spent_region, columns=['filepath','top_time','center_time','left_time','right_time'], index=[0])

    return des_df, ymaze_mouse[['time_diff', 'region']]


'''
Organizes maze coordinates for function use. 
'''


def main():
    path = r'/Users/colinmason/Desktop/yorglab/rat_maze_sim/CPP Experiment Data/Day 1/8003_CPP_cocaine_white _maze.behavior'
    mouse_df = pd.read_csv(path, header=2, sep='\t')
    edge_col = mouse_edge_distance(mouse_df, colin_sub_funcs.shapes('corridor'), .1)
    edge_col['change_sign'] = np.sign(edge_col['mouse_from_wall_units'])
    print(edge_col.groupby('change_sign')['mouse_from_wall_units'].max())


if __name__ == "__main__":
    main()





