import os
import pandas as pd
from shapely.geometry import Point
from shapely.geometry import Polygon, LineString
import numpy as np

# Gets fed the master sheet and maze coordinates. Distance threshold can be changed in the master sheet function.
def mouse_edge_distance(df_input, maze_coordinates, distance_threshold=35):

    df_test = df_input

    # Checks if coordinates are a circle radius.
    if isinstance(maze_coordinates, int):
        p = Point(0, 0)
        polygon_maze = p.buffer(maze_coordinates)

    else:
        polygon_maze = Polygon(maze_coordinates)

    # Checks coordinates in each row and returns the mouses distance from the edge and True or False if mouse is
    # within the threshold distance to the wall
    df_test["mouse_dist"] = df_test.apply(lambda row: polygon_maze.exterior.distance(Point(row["Position.X"], row["Position.Y"])), axis=1)
    df_test['distance_marked'] = df_test.apply(lambda row: 1 if distance_threshold >= row['mouse_dist'] else 0, axis=1)

    # Returns the entire master dataframe with mouse_dist and distance_marked as two new columns
    return df_test

# Function created for use in the y_maze_time_spent() function

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
        return np.nan


# Input is the behavioral data.

def y_maze_time_spent(behavioral_df):
    # Separates each region as different polygons
    top = Polygon(LineString([(-125, 513.924), (-125, 13.925), (125, 13.925), (125, 513.924), (-125, 513.924)]))
    center = Polygon(LineString([(0, -202.582), (-125, 13.925), (125, 13.925), (0, -202.582)]))
    left = Polygon(LineString([(-125, 13.925), (-558.013, -236.075), (-433.013, -452.582), (0, -202.582), (-125, 13.925)]))
    right = Polygon(LineString([(125, 13.925), (558.013, -236.075), (433.013, -452.582), (0, -202.582), (125, 13.925)]))

    ymaze_mouse = behavioral_df

    # New column that gets the difference between row (n) and row (n-1)
    ymaze_mouse['time_diff'] = ymaze_mouse['#Snapshot Timestamp'].diff()

    # Labels the different region in a dictionary
    regions_dict = {'top': top, 'center': center, 'left': left, 'right': right}
    time_spent_region = {}

    # Uses the key value pairs of regions_dict to label which region each coordinate resides
    # Lastly sums up the time spent in each region as a second dictionary
    for key, value in regions_dict.items():
        ymaze_mouse[key] = ymaze_mouse.apply(lambda row: value.contains(Point(row["Position.X"], row["Position.Y"])),axis=1)
        time_spent_region[key] = ymaze_mouse[ymaze_mouse[key] == True]['time_diff'].sum()

    # Applies the region_match function to each row and gives a string label for where the coordinate was found
    ymaze_mouse['region'] = ymaze_mouse.apply(region_match, axis=1)

    # New output df with the labelled columns

    out_df = ymaze_mouse.drop(columns=['top', 'center', 'left', 'right'])

    new_names = {'center': 'center_time', 'left': 'left_time', 'right': 'right_time', 'top': 'top_time'}

    # Final output dictionary with labels
    time_spent_region = dict((new_names[key], value) for (key, value) in time_spent_region.items())

    # outputs dictionary with labels of time spent in each region.
    # Also outputs a comprehensive dataframe with time_diff and region label added as columns
    return time_spent_region, out_df





