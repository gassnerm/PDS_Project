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

    print(series_timedelta.keys())
    print(series_timedelta)
    # return a series with duration in minutes for each trip
    return pd.Series(data=list(map(lambda x: pd.to_timedelta(series_timedelta[x]).total_seconds()/60, series_timedelta.index)))


# method to perform cleaning data frame from wrong data.
def drop_short_trips(df):

    df = pd.DataFrame(df)

    short_trip = df[list(map(lambda x: (df.loc[x]["duration"] <= float(180)) & (df.loc[x]["End_position_UID"] == df.loc[x]["Start_position_UID"]), df.index))]
    # drop short values from data frame
    df.drop(short_trip.index, inplace=True)
    return df


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
    missing_island = pd.DataFrame(df[df["p_name"].str.contains("^(Missing)")])
    df.drop(missing_island.index, inplace=True)

    return df


# Cleaning of new data frame
def cleaning_new_df(df):

    df = pd.DataFrame(df)

    # Drop trips with recording in place name
    recording_df = pd.DataFrame(df[df["Start_Place"].str.contains("^(recording)")])
    df.drop(recording_df.index, inplace=True)

    # Drop trip with negative lat or long position in england
    negative_df = pd.DataFrame(df[(df["Start_Latitude"].astype(float) < 0) | (df["Start_Longitude"].astype(float) < 0)])
    df.drop(negative_df.index, inplace=True)

    return df


def create_zip_code_data(df, geo_data):

    df_new = pd.DataFrame(df)
    zip_code = pd.DataFrame(geo_data)

    print(df_new)

    # create column for join
    df_new["Coordinates"] = df_new["Start_Latitude"].str.cat(df_new["Start_Longitude"], sep=", ")

    # join the zip code column based on lat long Coordinates
    df_new = df_new.join(zip_code, on=["Coordinates"], lsuffix="_s", )

    # drop trips with wrong coordinates
    wrong_coordinates = df_new[df_new["zipcodes"].astype(str).str.contains("^(?![0-9]{5})")].index
    df_new = df_new.drop(wrong_coordinates)

    # drop bookings they are not in frankfurt
    not_in_frankfurt = df_new[(df_new["zipcodes"].astype(int) > 65936) | (df_new["zipcodes"].astype(int) < 60306)].index
    df_new = df_new.drop(not_in_frankfurt)
    print(df_new)
    return df_new
