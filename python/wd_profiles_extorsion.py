import os
import pandas as pd

wd_pop = "/home/deras/Desktop/Midrar_work/thesis_work/feeder_model/basecase/final_files/"

def export_wd_files(wd_pop):
    counter = 1
    for files in os.listdir(wd_pop):
        if files.startswith("wd_"):
            df = pd.read_csv(os.path.join(wd_pop, files), names=['time','gpm'], parse_dates=True)
            df['time'] = pd.to_datetime(df['time'])
            df.set_index('time', inplace=True)
            for day in df.index.day.unique():
                day_df = df[df.index.day == day]
                new_range = pd.date_range(start=f"2021-12-25 00:00:00", end=f"2021-12-25 23:59:00", freq='1T')
                print('len old --> ',len(day_df.index), 'len new --> ', len(new_range), 'issue here -->',files)
                if len(day_df.index) == len(new_range):
                    day_df.index = new_range
                    day_df.to_csv(f"../wd_files/wd_{counter}.csv", header=False)
                    counter += 1
                else:
                    pass

    # counter = 1
    # for files in os.listdir(wd_pop):
    #     if files.startswith("wd_"):
    #         df = pd.read_csv(wd_pop+files, names=['time','gpm'], parse_dates=True)
    #         df['time'] = pd.to_datetime(df['time'])
    #         df.set_index('time', inplace=True)
    #         for day in df.index.day.unique():
    #             day_df = df[df.index.day == day]
    #             new_range = pd.date_range(start=f"2021-12-25 00:00:00", end=f"2021-12-25 23:59:00", freq='1T')
    #             day_df.index = new_range
    #             day_df.to_csv(f"../wd_files/wd_{counter}.csv")
    #             counter +=1


def main(wd_pop):
    export_wd_files(wd_pop)
main(wd_pop)