import os
import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt


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
def drop_short_long_trips(df):

    df = pd.DataFrame(df)

    # search for trips where the duration is under or equal 3 minutes and the position doesnt changed
    short_trip = df[(df["duration"] <= float(3)) & (df["End_position_UID"] == df["Start_position_UID"])]
    long_trips = df[(df["duration"] > float(120))]

    # drop short values from data frame
    df.drop(short_trip.index, inplace=True)
    df.drop(long_trips.index, inplace=True)

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

    # load geo data index are location coordinates
    zip_code = pd.DataFrame(geo_data)

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

    return df_new


def drop_outlier(df):
    print(df)

    # extract the month out of date
    df["month"] = df["Starttime"].astype(str).str.extract(pat="(-[0-9]{2}-)")
    df["month"] = df["month"].str.replace("-*-", "")

    # Separate the df by month
    Stat_Ja = df[df["month"] == "01"]
    Stat_Fe = df[df["month"] == "02"]
    Stat_Ma = df[df["month"] == "03"]
    Stat_Ap = df[df["month"] == "04"]
    Stat_May = df[df["month"] == "05"]
    Stat_Ju = df[df["month"] == "06"]
    Stat_Jul = df[df["month"] == "07"]
    Stat_Au = df[df["month"] == "08"]
    Stat_Se = df[df["month"] == "09"]
    Stat_Oc = df[df["month"] == "10"]
    Stat_No = df[df["month"] == "11"]
    Stat_De = df[df["month"] == "12"]

    fig, ax = plt.subplots(nrows=3, ncols=4, figsize=(20, 5))

    result_Januar = ax[0][0].boxplot(Stat_Ja["duration"].astype(float))
    result_Februar = ax[0][1].boxplot(Stat_Fe["duration"].astype(float))
    result_March = ax[0][2].boxplot(Stat_Ma["duration"].astype(float))

    result_April = ax[0][3].boxplot(Stat_Ap["duration"].astype(float))
    result_May = ax[1][0].boxplot(Stat_May["duration"].astype(float))
    result_June = ax[1][1].boxplot(Stat_Ju["duration"].astype(float))

    result_August = ax[1][2].boxplot(Stat_Au["duration"].astype(float))
    result_September = ax[1][3].boxplot(Stat_Se["duration"].astype(float))

    result_October = ax[2][0].boxplot(Stat_Oc["duration"].astype(float))
    result_November = ax[2][1].boxplot(Stat_No["duration"].astype(float))
    result_December = ax[2][2].boxplot(Stat_De["duration"].astype(float))

    #plt.savefig("data/boxplot-with-outlier.pdf")

    no_outliner_Ja = Stat_Ja[Stat_Ja["duration"].astype(float) <= result_Januar["whiskers"][1].get_ydata()[1]]
    no_outliner_Fe = Stat_Fe[Stat_Fe["duration"].astype(float) <= result_Februar["whiskers"][1].get_ydata()[1]]
    no_outliner_Ma = Stat_Ma[Stat_Ma["duration"].astype(float) <= result_March["whiskers"][1].get_ydata()[1]]
    no_outliner_Ap = Stat_Ap[Stat_Ap["duration"].astype(float) <= result_April["whiskers"][1].get_ydata()[1]]
    no_outliner_May = Stat_May[Stat_May["duration"].astype(float) <= result_May["whiskers"][1].get_ydata()[1]]
    no_outliner_Ju = Stat_Ju[Stat_Ju["duration"].astype(float) <= result_June["whiskers"][1].get_ydata()[1]]
    no_outliner_Au = Stat_Au[Stat_Au["duration"].astype(float) <= result_August["whiskers"][1].get_ydata()[1]]
    no_outliner_Se = Stat_Se[Stat_Se["duration"].astype(float) <= result_September["whiskers"][1].get_ydata()[1]]
    no_outliner_Oc = Stat_Oc[Stat_Oc["duration"].astype(float) <= result_October["whiskers"][1].get_ydata()[1]]
    no_outliner_No = Stat_No[Stat_No["duration"].astype(float) <= result_November["whiskers"][1].get_ydata()[1]]
    no_outliner_De = Stat_De[Stat_De["duration"].astype(float) <= result_December["whiskers"][1].get_ydata()[1]]

    # create the df without outlier
    df_new = no_outliner_Ja.append(no_outliner_Fe).append(no_outliner_Ma).append(
        no_outliner_Ap).append(no_outliner_May).append(no_outliner_Ju).append(no_outliner_Au).append(
        no_outliner_Se).append(no_outliner_Oc).append(no_outliner_No).append(no_outliner_De)

    df_new.drop(columns="month", inplace=True)
    return df_new
