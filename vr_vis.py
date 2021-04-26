from mastersheet_mod_funcs import mouse_farm
from colin_funcs import shapes
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, LineString
from shapely.ops import linemerge, unary_union, polygonize
import numpy as np
import seaborn as sns


def mouse_path(mouse_df, maze_array):
    maze = Polygon(shapes(maze_array))
    sns.scatterplot(x='Position.X', y='Position.Y', marker='o', data=mouse_df)
    if maze_array == 'ymaze':
        line = [LineString([(0, -202.582), (-125, 13.925), (125, 13.925), (0, -202.582)]), maze.boundary]
        line = unary_union(line)
        line = linemerge(line)
        polygons = polygonize(line)
        for polygon in polygons:
            x, y = polygon.exterior.xy
            plt.plot(x, y)
    plt.show()


def time_regon_plot_ymaze(ymaze_dict):
    time = [float(i) for i in ymaze_dict.values()]
    sns.barplot(x=list(ymaze_dict.keys()), y=time)
    plt.show()




def main():
    x1 = mouse_farm(r'/Users/colinmason/Desktop/ymaze_run_2_23_21 (1).behavior', 'ymaze')
    return np.nan


if __name__ == "__main__":
    main()