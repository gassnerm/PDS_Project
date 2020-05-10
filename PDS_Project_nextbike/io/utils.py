import os
import pandas as pd
import datetime as dt
import numpy as np


def get_data_path():
    if os.path.isdir(os.path.join(os.getcwd(), 'data')):
        return os.path.join(os.getcwd(), 'data')
    elif os.path.isdir(os.path.join(os.getcwd(), "../data")):
        return os.path.join(os.getcwd(), "../data")
    else:
        raise FileNotFoundError


# Cast the duration from timedelta to number of minutes
def cast_timedelta_to_number(series_timedelta):

    df = pd.DataFrame(series_timedelta)
    # return a series with duration in minutes for each trip
    return pd.Series(data=list(map(lambda x: pd.to_timedelta(df.loc[x]["duration"]).total_seconds()/60, df.index)))


# method to perform cleaning data frame from wrong data.
def drop_short_trips(df):

    df = pd.DataFrame(df)
    short_trip = df[(df["duration"] <= dt.timedelta(minutes=3)) & (df["End_position_UID"] == df["Start_position_UID"])]
    # drop short values from data frame
    df.drop(short_trip.index, inplace=True)


# Clean df from wrong data
def clean_df(df):
    print(df)
    # create data frame
    df = pd.DataFrame(df)

    # take all columns to control for na values except p_number contain 0 for bike place
    null_columns = np.array(list(filter(lambda x: (str(x) != "p_number"), df.columns)))

    # drop all rows that contains na values in the columns
    df.loc[:, null_columns].dropna(axis=0, subset=null_columns, inplace=True)

    # drop all rows that contains recordings and missing island in place name
    # recording_df = pd.DataFrame(df[df["p_name"].str.contains("^(recording)")])
    missing_island = pd.DataFrame(df[df["p_name"].str.contains("^(Missing)")])

    # df.drop(recording_df.index, inplace=True)
    df.drop(missing_island.index, inplace=True)

    return df
