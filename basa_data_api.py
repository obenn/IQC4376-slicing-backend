import pandas as pd
import os

df = None

def init_df(csv_location=os.getenv('SLICING_DATA_LOCATION', 'basa_data.csv')):
    print("Loading df into memory")
    df = pd.read_csv(csv_location, low_memory=False)
    print("done")
    return df

def columns():
    return list(df)

def subset(beginning=0, end=None, columns=None):
    if not end:
        end=len(df.index),
    if not columns:
        columns=columns() 
    return df.loc[beginning:end, columns]
