import os
import numpy as np
import pandas as pd


wd_files = "/home/deras/Desktop/midrar_work_github/dhw-generator/outputs/"


def export_wd_files(wd_files, file_name):
    df = pd.read_csv(wd_files+file_name)
    df["timestamp"] = pd.to_timedelta(pd.to_datetime(df["end_time"]) - pd.to_datetime(df["start_time"]))
    
    new_data = {'timestamp':[], 'draw':[]}
    new_df = pd.DataFrame(new_data)

    elapsed_time = pd.Timedelta(0)
    sum_draw = 0

    for i, row in df.iterrows():
        elapsed_time += row['timestamp']
        sum_draw += row['draw']

        if elapsed_time >= pd.Timedelta('00:01:00'):
            new_row = {'timestamp':pd.Timedelta('00:01:00'), 'draw':sum_draw}
            new_df = new_df.append(new_row, ignore_index=True)
            elapsed_time = elapsed_time - pd.Timedelta('00:01:00')
            sum_draw = 0
    new_df['timestamp'] = df['start_time']
    
    return new_df

def create_full_day_df(df):

    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.floor('min')

    data = {'timestamp':pd.date_range(start='2021-12-25 00:00:00', end='2021-12-25 23:59:00', freq='1T'),
            'draw':np.zeros(1440)}
    
    full_day_df = pd.DataFrame(data)

    merged_dfs = pd.merge(full_day_df, df, on='timestamp', how='left')
    
    merged_dfs['draw_x'] = merged_dfs['draw_x'].fillna(merged_dfs['draw_y'])

    merged_dfs = merged_dfs.drop('draw_x', axis=1)

    merged_dfs = merged_dfs.rename(columns={'draw_y':'draw'})

    merged_dfs['draw'] = (merged_dfs['draw'].fillna(0)).round(3)

    return merged_dfs

def wr_csv(df, file_counter):
    df.to_csv(f'wd_{file_counter}.csv')
    file_counter += 1

def main(wd_files):

    file_counter = 1

    for file_name in os.listdir(wd_files):

        df = export_wd_files(wd_files, file_name)

        df = create_full_day_df(df)

        wr_csv(df, file_counter)

main(wd_files)