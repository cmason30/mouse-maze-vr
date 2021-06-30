import matplotlib.pyplot as plt
from shapely.geometry import Polygon, LineString
from shapely.ops import linemerge, unary_union, polygonize
import seaborn as sns
import numpy as np

# ------------ Helper functions for visualizations --------#
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


# ------------- Visualization functions --------------------- #

def mouse_movement(mouse_df, maze_array, save_path=None):
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




def main():
    print('Running visualizations')


if __name__ == "__main__":
    main()