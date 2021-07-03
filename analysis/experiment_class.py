import numpy as np
import pandas as pd


class Experiment:
    def __init__(self, mouse_df):
        self.df = mouse_df

    def overall_time(self, units):
        self.df['distance_marked'] = np.where(self.df['mouse_from_wall_units'] < 34 + units, 1, 0)
        sum = self.df[self.df['distance_marked'] == 1]['time_diff'].sum()
        wall_percent = sum / 900

        wall_dict = {'sum': sum, '%_near_wall': wall_percent, 'units': units}

        return wall_dict

