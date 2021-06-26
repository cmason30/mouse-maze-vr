from main import mouse_farm
from colin_sub_funcs import shapes
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, LineString
from shapely.ops import linemerge, unary_union, polygonize
import seaborn as sns


def mouse_path(mouse_df, maze_array, save_path=None):
    maze = Polygon(shapes(maze_array))
    fig = plt.figure()
    if maze_array == 'ymaze':
        line = [LineString([(0, -202.582), (-125, 13.925), (125, 13.925), (0, -202.582)]), maze.boundary]
        line = unary_union(line)
        line = linemerge(line)
        polygons = polygonize(line)
        for polygon in polygons:
            x, y = polygon.exterior.xy
            plt.plot(x, y)
    sns.lineplot(x='Position.X', y='Position.Y', data=mouse_df, linewidth=.3)
    plt.show()
    if save_path is not None:
        fig.savefig(save_path)



def time_regon_plot_ymaze(ymaze_dict):
    time = [float(i) for i in ymaze_dict.values()]
    sns.barplot(x=list(ymaze_dict.keys()), y=time)
    plt.show()


# TODO: Update time_region_plot_ymaze to read dataframe instead of dictionary.

def main():
    x1 = mouse_farm(r'/Users/colinmason/Desktop/yorglab/rat_maze_sim/CPP Experiment Data/Day 1/8003_CPP_cocaine_white _maze.behavior', 'corridor')

    mouse_path(x1[0], 'corridor')

if __name__ == "__main__":
    main()