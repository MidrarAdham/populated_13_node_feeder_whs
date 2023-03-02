import os
import random
import numpy as np
import pandas as pd

wd_files = "/home/deras/Desktop/midrar_work_github/populated_13_node_feeder_whs/wd_files/renamed_three_gallons/"
wd_pop = "/home/deras/Desktop/Midrar_work/thesis_work/feeder_model/basecase/final_files/"
# df = pd.read_csv(wd_pop+"wd_1.csv",names = ['timestamp', 'gpm'])
# df = df.drop(['gpm'], axis=1)
# def pop_wd_files(wd_pop):
#     for files in os.listdir(wd_pop):
#         if files.startswith('wd_'):
#             timestamps = df['timestamp'].sample(20, replace=False, random_state=42)
#             new_demands = np.random.randint(1, 9, size=len(timestamps))
#             for i, ts in enumerate(timestamps):
#                 df.loc[df['timestamp'] == ts, 'demand'] = new_demands[i]
#                 df = df.fillna(0)
#                 df['demand'] = df['demand'].fillna(0)


# read the CSV file with timestamp column
df = pd.read_csv(wd_pop+"wd_1.csv",names = ['timestamp', 'demand'], parse_dates=['timestamp'])

# set the timestamp column as the index
df = df.set_index('timestamp')

# create a new demand column with zeros
df['demand'] = 0

# generate demand values using the Poisson distribution
demand_values = np.random.poisson(1, size=len(df))

# create a mask for the time range between 6 am and 8 am
mask = (df.index.hour >= 6) & (df.index.hour < 8)

# adjust the demand values for the time range between 6 am and 8 am
demand_values[mask] = np.random.poisson(5, size=mask.sum())

# assign the demand values to the demand column
df['demand'] = demand_values

# save the modified DataFrame to a new CSV file
df.to_csv('test.csv')



# def resample_ts(wd_files):
#     df = pd.read_csv(wd_files+"wd_18_3.csv")
    
#     df['timestamp'] = pd.to_datetime(df['timestamp'])

#     df.set_index('timestamp', inplace=True)

#     df = df.resample('1T').ffill()

#     return df



# def adjust_gpm(new_df):
#     # Adjust the demand column to account for the duration
#     new_df['demand(gpm)'] *= new_df['duration(sec)'] / 60

#     new_df['demand(gpm)'] = new_df['demand(gpm)'].round(2)
#     new_df['demand(gpm)'] = (new_df['demand(gpm)'].fillna(0)).astype(int)
#     # Drop the duration column
#     new_df.drop('duration(sec)', axis=1, inplace=True)

#     new_df = masking(new_df)
#     # Reset the index
#     new_df.reset_index(inplace=True)

#     return new_df
    

# def masking(new_df):
#     # Scale data: Remove gpm that are less than 1. GridLAB-D ignores them. (<--doublecheck)
#     new_df['demand(gpm)'] = new_df['demand(gpm)'].mask(new_df['demand(gpm)'] < 1, 0)
    
#     mask = new_df['demand(gpm)'] >= 16
#     counts = mask.cumsum()[mask]
#     values_to_replace = counts[counts > 1].index.values
#     new_df.loc[values_to_replace[0:], 'demand(gpm)'] = 0

#     mask = new_df['demand(gpm)'] >= 1
#     counts = mask.cumsum()[mask]
#     values_to_replace = counts[counts > 3].index.values
#     new_df.loc[values_to_replace[10:], 'demand(gpm)'] = 0
    
#     return new_df


# def full_day_col(df):

#     new_ts = pd.date_range('2023-01-01 00:00:00','2023-01-01 23:59:59', freq = '1min')
#     new_df = pd.DataFrame(new_ts)
#     new_df.columns = ['timestamp']
#     new_df = pd.concat([new_df, df['demand(gpm)']], axis=1)
#     new_df['demand(gpm)'] = (new_df['demand(gpm)'].fillna(0)).astype(int)
#     return new_df

# def test_output(df):
#     df.to_csv('test.csv', index=False)

# def main(wd_files, wd_pop):
#     df = pop_wd_files(wd_pop)
    
    # df = resample_ts(wd_files)
    # df = adjust_gpm(df)
    # df = full_day_col(df)
    # test_output(df)
# main(wd_files, wd_pop)
