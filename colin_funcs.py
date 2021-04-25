import pandas as pd
from shapely.geometry import Point
from shapely.geometry import Polygon, LineString, LinearRing
import numpy as np

# Gets fed the master sheet and maze coordinates.
# dist_threshold has to be between 0 and 1

def mouse_edge_distance(df_input, maze_coordinates, distance_threshold=.9):
    df_test = df_input.copy()

    # Checks if coordinates are a circle radius.
    if isinstance(maze_coordinates, int):
        p = Point(0, 0)
        inner_circle = maze_coordinates * distance_threshold
        polygon_maze = p.buffer(maze_coordinates)
        red_poly_main = polygon_maze.difference(Point(0.0, 0.0).buffer(inner_circle)) # <- donut

    else:
        ident_mat = np.zeros((2, 2), float)
        np.fill_diagonal(ident_mat, distance_threshold)
        coords_t = maze_coordinates.transpose()
        coords_red = np.matmul(ident_mat, coords_t)
        polygon_maze = Polygon(maze_coordinates)
        red_lin = LinearRing(coords_red.transpose())
        red_poly_main = Polygon(maze_coordinates, [red_lin])

    # Checks coordinates in each row and returns the mouses distance from the edge and True or False if mouse is
    # within the threshold distance to the wall
    df_test["mouse_dist"] = df_test.apply(lambda row: polygon_maze.exterior.distance(Point(row["Position.X"], row["Position.Y"])), axis=1)
    df_test['distance_marked'] = df_test.apply(lambda row: 1 if red_poly_main.contains(Point(row["Position.X"], row["Position.Y"])) else 0, axis=1)

    # Checks that all coordinates are in Polygon
    df_test['in_poly'] = df_test.apply(lambda row: polygon_maze.contains(Point(row["Position.X"], row["Position.Y"])), axis=1)
    if (~df_test['in_poly']).sum() != 0:
        raise Exception('Warning! Mouse movement detected outside of Polygon boundaries.')

    # outputs two columns: mouse_dist, distance_marked
    return df_test[['mouse_dist', 'distance_marked']]

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
        raise Exception('Warning! Mouse movement detected outside of Polygon boundaries.')


# Input is the behavioral data.

def y_maze_time_spent(behavioral_df):
    # Separates each region as different polygons
    top = Polygon(LineString([(-125, 513.924), (-125, 13.925), (125, 13.925), (125, 513.924), (-125, 513.924)]))
    center = Polygon(LineString([(0, -202.582), (-125, 13.925), (125, 13.925), (0, -202.582)]))
    left = Polygon(LineString([(-125, 13.925), (-558.013, -236.075), (-433.013, -452.582), (0, -202.582), (-125, 13.925)]))
    right = Polygon(LineString([(125, 13.925), (558.013, -236.075), (433.013, -452.582), (0, -202.582), (125, 13.925)]))

    ymaze_mouse = behavioral_df.copy()

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
    first_time = ymaze_mouse['#Snapshot Timestamp'][0]
    first_region = ymaze_mouse['region'][0]
    time_spent_region[first_region] += first_time

    # New output df with the labelled columns

    out_df = ymaze_mouse.drop(columns=['top', 'center', 'left', 'right'])

    new_names = {'center': 'center_time', 'left': 'left_time', 'right': 'right_time', 'top': 'top_time'}

    # Final output dictionary with labels
    time_spent_region = dict((new_names[key], value) for (key, value) in time_spent_region.items())

    # outputs dictionary with labels of time spent in each region.
    # outputs df with 2 columns: time_diff, region
    return time_spent_region, out_df[['time_diff', 'region']]







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
    print(sum(y_maze_time_spent(df_test_ymaze)[0].values()))
    # print(df_test_ymaze['#Snapshot Timestamp'][0] + y_maze_time_spent(df_test_ymaze)[1]['time_diff'].sum())
    # time = 180.017000



if __name__ == "__main__":
    main()





