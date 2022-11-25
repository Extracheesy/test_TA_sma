import numpy as np
import pandas as pd
from stockstats import StockDataFrame as Sdf
from finta import TA

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def build_random_df():
    np.random.seed(0)

    lst_column = ['close', 'open', 'low', 'high']
    df = pd.DataFrame(np.random.randint(0, 1000, size=(1000, 4)), columns=lst_column)

    return df

if __name__ == '__main__':
    df = build_random_df()

    stock = Sdf.retype(df.copy())
    period = int(400)
    df["ema_400"] = TA.EMA(stock, period=period).copy()
    df["ema_400_incremental"] = 0

    exit_flag = False
    interval_start = -400
    interval_end = interval_start + period + 1
    while not exit_flag:
        df2 = df[max(0, interval_start):interval_end].copy()
        stock = Sdf.retype(df2.copy())

        df2["ema_400_incremental"] = TA.EMA(stock, period=period).copy()

        df.loc[df.index == interval_end-1, 'ema_400_incremental'] = df2.loc[interval_end-1, 'ema_400_incremental']
        if interval_end > len(df) - 1:
            exit_flag = True
        interval_start += 1
        interval_end += 1

    df.to_csv('ema_400_vs.csv')
    print_hi('PyCharm')
