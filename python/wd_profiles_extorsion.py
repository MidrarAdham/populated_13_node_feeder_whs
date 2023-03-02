import os
import pandas as pd

wd_pop = "/home/deras/Desktop/Midrar_work/thesis_work/feeder_model/basecase/final_files/"

def export_wd_files(wd_pop):
    counter = 1
    for files in os.listdir(wd_pop):
        if files.startswith("wd_"):
            df = pd.read_csv(wd_pop+files, names=['time','gpm'], parse_dates=True)
            df['time'] = pd.to_datetime(df['time'])
            df.set_index('time', inplace=True)
            for day in df.index.day.unique():
                day_df = df[df.index.day == day]
                day_df.to_csv(f"../wd_files/wd_{counter}.csv")
                counter +=1


def main(wd_pop):
    export_wd_files(wd_pop)
main(wd_pop)