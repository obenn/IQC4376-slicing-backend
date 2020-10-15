import pandas as pd
import os

def init_df(csv_location=os.getenv('SLICING_DATA_LOCATION', 'basa_data.csv')):
    print("Loading df into memory")
    df = pd.read_csv(csv_location, low_memory=False)
    print("done")
    return df

df = init_df()

def columns():
    return list(df)

def subset(beginning=0, end=len(df.index), columns=columns()):
    return df.loc[beginning:end, columns]
