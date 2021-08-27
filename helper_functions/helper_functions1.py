import pandas as pd
import PySimpleGUI as sg
from shapely.geometry import Point
from shapely.geometry import Polygon, LineString, LinearRing
import numpy as np
from helper_functions import helper_functions2
import os

# ------------ First line functions ----------------------- #
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

'''
Organizes maze coordinates for function use. 
'''

def shapes(maze_array, plotly=False):
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

            if plotly:
                x, y = coords.T
                x = np.append(x, [-433.013])
                y = np.append(y, [-452.582])
                return x, y

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

    def within_bounds(df, polygon):
        df['in_poly'] = df.apply(lambda row: polygon.contains(Point(row["Position.X"], row["Position.Y"])), axis=1)
        if (~df['in_poly']).sum() != 0:
            raise Exception('Warning! Mouse movement detected outside of Polygon boundaries.')

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

def y_maze_regions(behavioral_df, maze_type):
    mouse_df = behavioral_df.copy()
    mouse_df['time_diff'] = mouse_df['#Snapshot Timestamp'].diff()

    def isin_region(row):
        top = Polygon(LineString([(-125, 513.924), (-125, 13.925), (125, 13.925), (125, 513.924), (-125, 513.924)]))
        center = Polygon(LineString([(0, -202.582), (-125, 13.925), (125, 13.925), (0, -202.582)]))
        left = Polygon(
            LineString([(-125, 13.925), (-558.013, -236.075), (-433.013, -452.582), (0, -202.582), (-125, 13.925)]))
        right = Polygon(
            LineString([(125, 13.925), (558.013, -236.075), (433.013, -452.582), (0, -202.582), (125, 13.925)]))

        if top.contains(Point(row["Position.X"], row["Position.Y"])):
            return 'top'

        elif center.contains(Point(row["Position.X"], row["Position.Y"])):
            return 'center'

        elif left.contains(Point(row["Position.X"], row["Position.Y"])):
            return 'left'

        elif right.contains(Point(row["Position.X"], row["Position.Y"])):
            return 'right'

        else:
            raise Exception(f'Points on {row["#Snapshot Timestamp"]} not found in any region for ymaze.')

    if maze_type == 'ymaze':
        region_times = {}
        mouse_df['region'] = mouse_df.apply(isin_region, axis=1)
        regions_grouped = mouse_df.groupby(['region'])
        for region, df in regions_grouped:
            region_times[region] = df['time_diff'].sum()

    else:
        mouse_df['region'] = None
        region_times = {'top': None, 'center': None, 'left': None, 'right': None}

    return mouse_df[['time_diff', 'region']], region_times




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
    settings = pd.read_csv(df_path, nrows=2, header=None, sep='\t')
    vrsettings = settings.iloc[0][0]
    mazesettings = settings.iloc[1][0]
    filename = os.path.basename(df_path)

    def drug_applied(path):
        if 'saline' in path:
            return 'saline'
        elif 'cocaine' in path:
            return 'cocaine'
        else:
            return None

    drug = drug_applied(df_path)
    wall_distance = mouse_edge_distance(mouse_df, maze_array, dist_threshold)
    speed = helper_functions2.calc_speed(mouse_df)
    ymaze_data = y_maze_regions(mouse_df, maze_array)
    region_times = ymaze_data[1]
    total_distance_traveled = total_distance(mouse_df[['Position.X', 'Position.Y']])

    mouse_df['filename'] = filename
    mouse_df['file_path'] = df_path
    mouse_df['maze_type'] = maze_array
    mouse_df['.vrsettings'] = vrsettings
    mouse_df['.mazesettings'] = mazesettings
    mouse_df['drug_applied'] = drug
    mouse_df['total_distance'] = total_distance_traveled
    mouse_df['top_time'] = region_times['top']
    mouse_df['center_time'] = region_times['center']
    mouse_df['left_time'] = region_times['left']
    mouse_df['right_time'] = region_times['right']

    final_df = pd.concat([mouse_df, wall_distance, speed, ymaze_data[0]], axis=1)
    # Columns of final df:['#Snapshot Timestamp', 'Trigger Region Identifier', 'Position.X',
    #        'Position.Y', 'Position.Z', 'Forward.X', 'Forward.Y', 'Forward.Z',
    #        'filename', 'file_path', 'maze_type', '.vrsettings', '.mazesettings',
    #        'drug_applied', 'total_distance', 'top_time', 'center_time',
    #        'left_time', 'right_time', 'dist_wall_units', 'distance_marked',
    #        'Speed', 'time_diff', 'region']

# JSON file of single-line metadata

    metadata_json = {'file_name': filename,
                     'file_path': df_path,
                     'maze': maze_array,
                     '.vrsetting': vrsettings,
                     '.maze': mazesettings,
                     'drug_applied': drug,
                     'distance_traveled': total_distance_traveled
                     }

    metadata_json = {**metadata_json, **region_times}

    return final_df, metadata_json


def generate_analyis(behavioral_filepath, maze_array, dist_threshold=.1, output_path=None):
    mouse_df = mouse_farm(behavioral_filepath, maze_array, dist_threshold)
    pathname = os.path.splitext(behavioral_filepath)[0]
    if output_path is None:
        mouse_df[0].to_csv(f'{pathname}_processed.csv')
        mouse_df[1].to_json(f'{pathname}_additional_data.json', orient="index")

    # elif output_path is not None:
    #     mouse_df[0].to_csv(f'{output_path}_processed.csv')
    #     mouse_df[1].to_json(f'{output_path}_experiment_data.json', orient="index")
    #     print('File processed.')

    else:
        print('Give a valid filepath.')






def main():


    path = r'/Users/colinmason/Desktop/yorglab/rat_maze_sim/CPP Experiment Data/Final Test Day/8002_CPP_y_maze__1.behavior'
    print(mouse_farm(path, 'ymaze')[0].columns)



if __name__ == "__main__":

    main()




