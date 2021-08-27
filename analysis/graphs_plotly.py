import plotly.express as px
import plotly.graph_objects as go
from helper_functions import helper_functions1
import plotly.io as pio
# pio.renderers.default = "svg"


class Experiment:
    def __init__(self, behavioral_path):
        self.mouse_data = helper_functions1.mouse_farm(behavioral_path)
        self.df = self.mouse_data[0]
        self.metadata = self.mouse_data[1]
        self.shape = self.metadata['maze_type']

    def export_data(self):
        pass

    def movement_plot(self):
        df = self.df

        bound_x, bound_y = helper_functions1.shapes(self.shape, plotly=True)
        fig = px.scatter(df, x='Position.X', y='Position.Y', color='region')
        fig.add_trace(go.Scatter(x=bound_x, y=bound_y))

        if self.shape == 'Y_Maze':
            sep_x = [0, -125, 125, 0]
            sep_y = [-202.582, 13.925, 13.925, -202.582]
            fig.add_trace(go.Scatter(x=sep_x, y=sep_y))



        fig.show()


animal1 = Experiment(r'/Users/colinmason/Desktop/yorglab/rat_maze_sim/CPP Experiment Data/Final Test Day/8002_CPP_y_maze__1.behavior')
animal1.movement_plot()


