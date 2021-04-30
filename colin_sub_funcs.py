from shapely.geometry import Point
from shapely.geometry import Polygon, LineString, LinearRing
import numpy as np

# ----------- Functions for use in mouse_edge_distance() ------------ #

'''
Creates polygon of maze and inner maze for boundary separation. 

Output 
polygon_maze: Polygon of entire maze boundaries
reduced_poly: Inner threshold polygon to detect mouse near wall

'''

def shape_shrink(maze_coordinates, distance_threshold):
    distance_val = 1 - distance_threshold
    if isinstance(maze_coordinates, int):
        p = Point(0, 0)
        inner_circle = maze_coordinates * distance_val
        polygon_maze = p.buffer(maze_coordinates)
        reduced_poly = polygon_maze.difference(Point(0.0, 0.0).buffer(inner_circle))  # <- donut

    else:
        ident_mat = np.zeros((2, 2), float)
        np.fill_diagonal(ident_mat, distance_val)
        coords_t = maze_coordinates.transpose()
        coords_red = np.matmul(ident_mat, coords_t)
        polygon_maze = Polygon(maze_coordinates)
        red_lin = LinearRing(coords_red.transpose())
        reduced_poly = Polygon(maze_coordinates, [red_lin])

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
