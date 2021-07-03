import pandas as pd
import PySimpleGUI as sg
from shapely.geometry import Point
from shapely.geometry import Polygon, LineString, LinearRing
import numpy as np
from helper_functions import helper_functions2
import os

# ------------ First line functions ----------------------- #
"""
Creates rug applied column data

"""
def drug_applied(path):
    if 'saline' in path:
        return 'saline'
    elif 'cocaine' in path:
        return 'cocaine'
    else:
        return None



"""
Creates pairing_info column data


"""


def pairing_info(path):
    if 'saline' in path:
        return 'saline'
    elif 'cocaine' in path:
        return 'cocaine'
    else:
        return None


def shape_shrink(maze_polygon, distance_threshold):
    distance_val = 1 - distance_threshold
    if isinstance(maze_polygon, int):
        p = Point(0, 0)
        inner_circle = maze_polygon * distance_val
        polygon_maze = p.buffer(maze_polygon)
        reduced_poly = polygon_maze.difference(Point(0.0, 0.0).buffer(inner_circle))  # <- donut

    else:
        ident_mat = np.zeros((2, 2), float)
        np.fill_diagonal(ident_mat, distance_val)
        coords_t = maze_polygon.transpose()
        coords_red = np.matmul(ident_mat, coords_t)
        polygon_maze = Polygon(maze_polygon)
        red_lin = LinearRing(coords_red.transpose())
        reduced_poly = Polygon(maze_polygon, [red_lin])

    return polygon_maze, reduced_poly



'''
Checks that coordinates are in entire maze. 
'''


def within_bounds(df, polygon):
    df['in_poly'] = df.apply(lambda row: polygon.contains(Point(row["Position.X"], row["Position.Y"])), axis=1)
    if (~df['in_poly']).sum() != 0:
        raise Exception('Warning! Mouse movement detected outside of Polygon boundaries.')


# ----------- Functions for use in y_maze_time_spent() ------------ #

def region_match(row):
    if row['top']:
        return 'top'
    elif row['center']:
        return 'center'
    elif row['right']:
        return 'right'
    elif row['left']:
        return 'left'
    else:
        raise Exception('Warning! Mouse coordinates found outside of all ymaze regions.')



'''
Organizes the coordinates for each ymaze region in a dictionary with region name as keys and coordinates as values
'''

def regions_dictionary():
    top = Polygon(LineString([(-125, 513.924), (-125, 13.925), (125, 13.925), (125, 513.924), (-125, 513.924)]))
    center = Polygon(LineString([(0, -202.582), (-125, 13.925), (125, 13.925), (0, -202.582)]))
    left = Polygon(LineString([(-125, 13.925), (-558.013, -236.075), (-433.013, -452.582), (0, -202.582), (-125, 13.925)]))
    right = Polygon(LineString([(125, 13.925), (558.013, -236.075), (433.013, -452.582), (0, -202.582), (125, 13.925)]))

    return {'top': top, 'center': center, 'left': left, 'right': right}


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







# ---------- Second order functions ------------------------------------------------------ #

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
    shape = shapes(maze_name)

    # Gets inner shape to make distance threshold boundary polygons
    polygon_maze, reduced_poly = shape_shrink(shape, distance_threshold)

    # Checks coordinates in each row and returns the mouses distance from the edge and True or False if mouse is
    # within the threshold distance to the wall
    df_test["dist_wall_units"] = df_test.apply(lambda row: polygon_maze.exterior.distance(Point(row["Position.X"], row["Position.Y"])) - 33.9, axis=1)
    df_test['distance_marked'] = df_test.apply(lambda row: 1 if reduced_poly.contains(Point(row["Position.X"], row["Position.Y"])) else 0, axis=1)

    # Checks that all coordinates are in Polygon
    within_bounds(df_test, polygon_maze)

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
        regions_coordinates = regions_dictionary()

    # Uses the key value pairs of regions_dict to label which region each coordinate resides
    # Lastly sums up the time spent in each region as a second dictionary

        for key, value in regions_coordinates.items():

            ymaze_mouse[key] = ymaze_mouse.apply(lambda row: value.contains(Point(row["Position.X"], row["Position.Y"])),axis=1)
            time_spent_region[key] = ymaze_mouse[ymaze_mouse[key] == True]['time_diff'].sum()

    # Applies the region_match function to each row and gives a string label for where the coordinate was found
        ymaze_mouse['region'] = ymaze_mouse.apply(region_match, axis=1)
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
                'top_time': None,
                'center_time': None,
                'left_time': None,
                'right_time': None,
                'maze_type': maze_type
                }
        ymaze_mouse['region'] = np.nan

    des_df = pd.DataFrame(time_spent_region, columns=['filepath','top_time','center_time','left_time','right_time'], index=[0])

    return des_df, ymaze_mouse[['time_diff', 'region']]


"""
Gets total distance traveled for experiment

"""


def total_distance(behavioral_df):
    mouse_df = behavioral_df.copy()
    dx = (mouse_df['Position.X'] - mouse_df['Position.X'].shift())
    dy = (mouse_df['Position.Y'] - mouse_df['Position.Y'].shift())
    mouse_df['euclidean_dist'] = np.sqrt(dx ** 2 + dy ** 2)
    final_value = mouse_df['euclidean_dist'].sum()
    return pd.DataFrame([final_value], columns=['distance_traveled'])


# ---------------------------------------- Master sheet generator ------------------------------------------------ #

'''

Organizes the functions to create a dataframe with all the significant variables as columns. 

Input
df_path: Give the file path of the behavioral file of interest.
maze_array: Give one of four strings( 'square', 'circle', 'ymaze', 'corridor') based on the maze that the behavior file ran on
master_path: Give the file path of the master sheet so that the new data being generated in this function appends to it. If generating
a new master sheet, then just leave as None

Output
Outputs a dataframe with the comprehensive data from the statistical functions in the helper_functions files.
Also outputs a second dataframe with descriptive stats gives region times and speed/velocity 
'''

def mouse_farm(df_path, maze_array, dist_threshold=.1):
    mouse_df = pd.read_csv(df_path, header=2, sep='\t')
    # file_path = pd.read_csv(df_path).iloc[0, 0]
    file_name = df_path

    mouse_df['filepath'] = df_path
    mouse_df['maze_type'] = maze_array

    mouse_distance = mouse_edge_distance(mouse_df, maze_array, dist_threshold)
    mouse_df['speed'] = helper_functions2.calc_speed(mouse_df)

    mouse_df['drug_applied'] = mouse_df.apply(lambda row: drug_applied(row['filepath']), axis=1)
    # mouse_df['pairing_info'] = mouse_df.apply(lambda row: helper_functions1.pairing_info(row['filepath']), axis=1)

    time_spent = y_maze_time_spent(mouse_df, file_name, maze_array)
    total_distance_traveled = total_distance(mouse_df[['Position.X', 'Position.Y']])

    final_df = pd.concat([mouse_df, mouse_distance, time_spent[1]], axis=1)
    des_df_row = pd.concat([time_spent[0], helper_functions2.avg_velocity(mouse_df), total_distance_traveled], axis=1)

    des_df_row.insert(5, 'drug_applied', drug_applied(df_path))
    des_df_row.insert(5, 'maze_type', maze_array)

    mesg = 'File Input.'
    return final_df, des_df_row, mesg


def main():
    return None


if __name__ == "__main__":

    main()




