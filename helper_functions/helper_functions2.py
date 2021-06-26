import math

import pandas as pd


#===============================================================================
# YRegions
# Input: dataframe
# Output: df["Regions"], and regions dictionary
def y_regions (df):
    df = df.copy()

   # Checks Base
    def in_base(cx, cy):
        ax = -125
        ay = 13.925
        bx = 125
        by = 13.925
        rval = ((bx-ax)*(cy-ay) - (by-ay)*(cx-ax))
        if rval > 0:
            return True
        else:
            return False

# Checks Right
    def in_right(cx, cy):
        ax = 0
        ay = -202.582
        bx = 125
        by = 13.925
        rval = ((bx-ax)*(cy-ay) - (by-ay)*(cx-ax))
        if rval < 0:
            return True
        else:
            return False

  # Checks Left
    def in_left(cx, cy):
        ax = 0
        ay = -202.582
        bx = -125
        by = 13.925
        rval = ((bx-ax)*(cy-ay) - (by-ay)*(cx-ax))
        if rval > 0:
            return True
        else:
            return False

  # Checks Center
    def in_center(cx, cy):
      # Check if not in other regions
        if not in_base(cx,cy) and not in_left(cx,cy) and not in_right(cx, cy):
      # Check base, left, and right boundaries
            if (cy < 13.925) and (((-125 - 0)*(cy - -202.582) - (13.925 - -202.582)*(cx - 0)) < 0) and (((125 - 0)*(cy - -202.582) - (13.925 - -202.582)*(cx - 0)) > 0):
                return True
            else:
                return False

  # Create column of time difference
    df["Time_diff"] = df["#Snapshot Timestamp"].diff()

  # Dictionary that holds time per region
    dictRegionTime = {
        "Base": 0,
        "Right": 0,
        "Left": 0,
        "Center": 0,
    }

    regions = []
    for row_name, row in df.iterrows():
        x = row["Position.X"]
        y = row["Position.Y"]
        if in_base(x,y):
            regions.append("Base")
            if math.isnan(row["Time_diff"]):
                dictRegionTime["Base"] += row["#Snapshot Timestamp"]
            else:
                dictRegionTime["Base"] += row["Time_diff"]
        elif in_right(x,y):
            regions.append("Right")
            if math.isnan(row["Time_diff"]):
                dictRegionTime["Right"] += row["#Snapshot Timestamp"]
            else:
                dictRegionTime["Right"] += row["Time_diff"]
        elif in_left(x,y):
            regions.append("Left")
            if math.isnan(row["Time_diff"]):
                dictRegionTime["Left"] += row["#Snapshot Timestamp"]
            else:
                dictRegionTime["Left"] += row["Time_diff"]
        elif in_center(x,y):
            regions.append("Center")
            if math.isnan(row["Time_diff"]):
                dictRegionTime["Center"] += row["#Snapshot Timestamp"]
            else:
                dictRegionTime["Center"] += row["Time_diff"]
        else:
            regions.append("None")

    df["Region"] = regions

    return df["Region"], dictRegionTime
  
  
#===================================================================================
# calcSpeed
# Input: Dataframe
# Output: df["Speed"], and mean of df["Speed"]
def calc_speed(df):
    df = df.copy()

    df["X_diff"] = df["Position.X"].diff()
    df["Y_diff"] = df["Position.Y"].diff()
    df["Time_diff"] = df["#Snapshot Timestamp"].diff()

  # List of speeds
    speeds = [0.0,]

    dfTemp = df.iloc[1:,:]
    for row_name, row in dfTemp.iterrows():
        a = row["X_diff"]
        b = row["Y_diff"]
        t = row["Time_diff"]
    
    # Find c
        c = math.pow(a, 2) + math.pow(b, 2)
        c = math.sqrt(c)

    # Find speed and append to list
        speed = c / t
        speeds.append(speed)

  # Add column to dataframe
    df["Speed"] = speeds

    return df["Speed"]
  
  
#================================================================================
# AverageVelocity
# Input: Dataframe
# Output: Float Value of average velocity throughout entire simulation (cm/sec)
def avg_velocity(dataf):
    df = dataf.copy()
  
    # Find Total Path Length
    totalPathLength = 0

    df["X_diff"] = df["Position.X"].diff()
    df["Y_diff"] = df["Position.Y"].diff()

    dfsliced = df.iloc[1:,:]

    for row_name, row in dfsliced.iterrows():
        # a equals difference in x values
        a = row["X_diff"]
        aSquared = math.pow(a, 2)

    # b equals difference in y values
        b = row["Y_diff"]
        bSquared = math.pow(b, 2)

    # Calculate length traveled in interval, and add to pathLength
        tempLength = math.sqrt(aSquared + bSquared)
        totalPathLength += tempLength

    # Find Total Time
    totalTime_sec = df.iloc[(df.index.size - 1), 0]

    # Find Average Velocity
    avgVel = totalPathLength / totalTime_sec

    return pd.DataFrame([avgVel], columns=['avg_vel'])
  
  
#==============================================================================

