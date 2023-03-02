import os
import random
import numpy as np
import pandas as pd

wd_files = "/home/deras/Desktop/midrar_work_github/populated_13_node_feeder_whs/wd_files/renamed_three_gallons/"
wd_pop = "/home/deras/Desktop/Midrar_work/thesis_work/feeder_model/basecase/final_files/"
df = pd.read_csv(wd_pop+"wd_1.csv",names = ['timestamp', 'gpm'])
df = df.drop(['gpm'], axis=1)
# def pop_wd_files(wd_pop):
#     for files in os.listdir(wd_pop):
#         if files.startswith('wd_'):
#             df = pd.read_csv(wd_pop+files, names = ['timestamp', 'gpm'], parse_dates=['timestamp'])
#             new_demand = np.random.randint(1,12, size=len(timestamps))
#             timestamps = df['timestamp'].sample(8)
#             for i, ts in enumerate(timestamps):
#                 df.loc[df['timestamp'] == ts, 'gpm'] = new_demand
#     print(df)
            
# randomly select 10 timestamps from the timestamp column
timestamps = df['timestamp'].sample(10, replace=False, random_state=42)

# generate 10 random values between 1 and 12
new_demands = np.random.randint(1, 9, size=len(timestamps))

# assign the new demand values to the randomly selected timestamps
for i, ts in enumerate(timestamps):
    df.loc[df['timestamp'] == ts, 'demand'] = new_demands[i]
df = df.fillna(0)
df['demand'] = df['demand'].fillna(0)
df.to_csv("./test.csv", index=False)


def resample_ts(wd_files):
    df = pd.read_csv(wd_files+"wd_18_3.csv")
    
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    df.set_index('timestamp', inplace=True)

    df = df.resample('1T').ffill()

    return df



def adjust_gpm(new_df):
    # Adjust the demand column to account for the duration
    new_df['demand(gpm)'] *= new_df['duration(sec)'] / 60

    new_df['demand(gpm)'] = new_df['demand(gpm)'].round(2)
    new_df['demand(gpm)'] = (new_df['demand(gpm)'].fillna(0)).astype(int)
    # Drop the duration column
    new_df.drop('duration(sec)', axis=1, inplace=True)

    new_df = masking(new_df)
    # Reset the index
    new_df.reset_index(inplace=True)

    return new_df
    

def masking(new_df):
    # Scale data: Remove gpm that are less than 1. GridLAB-D ignores them. (<--doublecheck)
    new_df['demand(gpm)'] = new_df['demand(gpm)'].mask(new_df['demand(gpm)'] < 1, 0)
    
    mask = new_df['demand(gpm)'] >= 16
    counts = mask.cumsum()[mask]
    values_to_replace = counts[counts > 1].index.values
    new_df.loc[values_to_replace[0:], 'demand(gpm)'] = 0

    mask = new_df['demand(gpm)'] >= 1
    counts = mask.cumsum()[mask]
    values_to_replace = counts[counts > 3].index.values
    new_df.loc[values_to_replace[10:], 'demand(gpm)'] = 0
    
    return new_df


def full_day_col(df):

    new_ts = pd.date_range('2023-01-01 00:00:00','2023-01-01 23:59:59', freq = '1min')
    new_df = pd.DataFrame(new_ts)
    new_df.columns = ['timestamp']
    new_df = pd.concat([new_df, df['demand(gpm)']], axis=1)
    new_df['demand(gpm)'] = (new_df['demand(gpm)'].fillna(0)).astype(int)
    return new_df

def test_output(df):
    df.to_csv('test.csv', index=False)

# def main(wd_files, wd_pop):
#     df = pop_wd_files(wd_pop)
    
    # df = resample_ts(wd_files)
    # df = adjust_gpm(df)
    # df = full_day_col(df)
    # test_output(df)
# main(wd_files, wd_pop)
