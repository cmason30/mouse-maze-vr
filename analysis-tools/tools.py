import pandas as pd


'''
Turns behavioral file into dataframe

input: 
    behavioral_file_path: File path of behavioral file on your computer.
    
output:
    Pandas dataframe of behavioral file (ignores metadata of first two rows)
'''


def behavioral_to_df(behavioral_file_path):
    df = pd.read_csv(behavioral_file_path, header=2, sep='\t')
    return df


# file_path = r'/Users/colinmason/Desktop/yorglab/rat_maze_sim/CPP Experiment Data/Day 1/8002_CPP_cocaine_blue_maze.behavior'
# behavioral_to_df(file_path)





