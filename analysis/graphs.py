from helper_functions import helper_functions1
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, LineString
import seaborn as sns
from shapely.ops import linemerge, unary_union, polygonize


def mazeplot_corridor(mouse_df, dist_threshold=5):
    mouse_df['distance_marked'] = np.where(mouse_df['mouse_from_wall_units'] < 34+dist_threshold, f'<{dist_threshold} units', f'>{dist_threshold} units')
    maze_array = mouse_df['maze_type'].unique()[0]
    maze = Polygon(helper_functions1.shapes('corridor'))
    # plt.figure(figsize=(4,6))

    x, y = maze.exterior.xy
    plt.plot(x,y)
    ax = sns.scatterplot(x='Position.X', y='Position.Y', data=mouse_df, hue='distance_marked')
    ax.set_title(mouse_df['filepath'].unique()[0][66:])
    # ax.set(xlim=(-100,100))
    return ax


def mazeplot_ymaze(mouse_df):
    mouse_df['distance_marked'] = np.where(mouse_df['dist_wall_units'] < 34+5, '<5 units', '>5 units')
    maze_array = mouse_df['maze_type'].unique()[0]
    maze = Polygon(helper_functions1.shapes(maze_array))
    poly_line = [LineString([(0, -202.582), (-125, 13.925), (125, 13.925), (0, -202.582)]), maze.boundary]
    line = unary_union(poly_line)
    line = linemerge(line)
    polygons = polygonize(line)
    for polygon in polygons:
        x, y = polygon.exterior.xy
        plt.plot(x, y)
        ax = sns.scatterplot(x='Position.X', y='Position.Y', data=mouse_df, hue='distance_marked', linewidth=.3)
        ax.set_title(mouse_df['filepath'].unique()[0][66:])




test1 = helper_functions1.mouse_farm(r'/Users/colinmason/Desktop/yorglab/rat_maze_sim/CPP Experiment Data/Final Test Day/8002_CPP_y_maze__1.behavior', 'ymaze')

print(mazeplot_ymaze(test1[0]))



