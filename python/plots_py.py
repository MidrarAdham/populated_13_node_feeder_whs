import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.dates import MonthLocator, DateFormatter

# files = pd.read_csv('../output/archive/trip_node_meter_file_1.csv', skiprows=range(0,7))

files = pd.read_csv('../output/trip_node_meter_file_1.csv', skiprows=range(0,7))

def clean_csv(df):

    df['# timestamp'] = df['# timestamp'].apply(lambda x: x.rstrip('UTC'))
    return df

def plots(df):
    x = pd.to_datetime(df['# timestamp'])
    print(x)
    y = (df['trip_node_meter_0:measured_real_power'])
    fig, ax = plt.subplots(1,figsize=(12,8))
    ax.xaxis.set_major_locator(plt.MaxNLocator(20))
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
    plt.xticks(ha='right')
    ax.plot(x,y, label='Real Power (W)')
    legend_prop = {'weight':'bold'}
    plt.xticks(rotation=45)
    plt.legend(prop = legend_prop)
    plt.tight_layout()
    plt.show()


def main(files):
    df = clean_csv(files)
    plots(df)
    print(df)


main(files)