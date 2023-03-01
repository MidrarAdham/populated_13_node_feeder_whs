import os
import pandas as pd

wd_files = "/home/deras/Desktop/midrar_work_github/populated_13_node_feeder_whs/wd_files/renamed_three_gallons/"

def read_csv(wd_files):
    for files in os.listdir(wd_files):
        print(files)
        df = pd.read_csv(wd_files+files, usecols=['timestamp','demand(gpm)','duration(sec)','duration(min)'])
        
        break
        
    

    

def main(wd_files):
    read_csv(wd_files)

main(wd_files)

