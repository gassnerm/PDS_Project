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

    # return a series with duration in minutes for each trip
    return pd.Series(data=list(map(lambda x: pd.to_timedelta(series_timedelta[x]).total_seconds()/60, series_timedelta.index)))


# method to perform cleaning data frame from wrong data.
def drop_short_long_trips(df):

    df = pd.DataFrame(df)

    # search for trips where the duration is under or equal 3 minutes and the position doesnt changed
    short_trip = df[(df["Duration"] <= float(3)) & (df["End_position_UID"] == df["Start_position_UID"])]

    # write DF without reduction
    long_trips = df[(df["Duration"] > float(120))]

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
    wrong_coordinates = df_new[df_new["Zip_codes"].astype(str).str.contains("^(?![0-9]{5})")].index
    df_new = df_new.drop(wrong_coordinates)

    # drop bookings they are not in frankfurt
    not_in_frankfurt = pd.DataFrame(columns=["Zipcode"])
    for i in df_new.index:

        # zip_codes of frankfurt
        if (int(df_new.loc[i]["Zip_codes"]) in [60306, 60308, 60311, 60313, 60314, 60316, 60318,
                                            60320, 60322, 60323, 60325, 60326, 60327, 60329,
                                            60385, 60386, 60388, 60389, 60431, 60433, 60435,
                                            60437, 60438, 60439, 60486, 60487, 60488, 60489,
                                            60528, 60529, 60547, 60549, 60594, 60596, 60598,
                                            60599, 61352, 63067, 65929, 65931, 65933, 65934, 65936]):
            continue
        else:
            not_in_frankfurt.loc[i, "Zipcode"] = df_new.loc[i]["Zip_codes"]


    not_in_frankfurt

    df_new = df_new.drop(not_in_frankfurt.index)

    return df_new


# method to delete batch bookings
def drop_reallocation_trips(df):
    # get trips start times
    time_frames = pd.DataFrame(df["Start_Time"].value_counts())

    # get start times occur more then 4 times number of bikes that can be lent in parall
    time_frames = time_frames[time_frames["Start_Time"] > 4]

    # get bookings in df
    wrong = df[df["Start_Time"].isin(time_frames.index)].sort_values("Start_Time")

    # find bookings that has also same end
    time_frames_end = pd.DataFrame(df["End_time"].value_counts())

    # occur more then 4 times with same end
    time_frames_end = time_frames_end[time_frames_end["End_time"] > 4]

    # get the wrong trips with the same ends and starts with more then 4 occur
    wrong_eND = wrong[wrong["End_time"].isin(time_frames_end.index)]

    # get statistics of bookings
    wrong_eND.groupby("Start_Time")["Duration"].mean()
    wrong_eND.groupby("Start_Time")["Duration"].count()
    wrong_eND.groupby("Start_Time")["Duration"].min()

    # orchestrate statistics to data frame
    wrong_data = pd.DataFrame(columns=["Mean", "Count", "min"], index=wrong_eND["Start_Time"],
                              data={"Mean": wrong_eND.groupby("Start_Time")["Duration"].mean(),
                                    "min": wrong_eND.groupby("Start_Time")["Duration"].min(),
                                    "Count": wrong_eND.groupby("Start_Time")["Duration"].count()})

    # get dates that has to be dropped
    true = wrong_data.groupby("Start_Time").max().sort_values("min")["Count"] > 4

    start_time = true.index.astype(str)

    # drop trip from data frame
    df.drop(df[df["Start_Time"].isin(start_time)].index, inplace=True)
    return df


# method to drop every outlier that is as far away from the times 1.5 distanz to the 25 and the 75 quantile
def drop_outlier(df):
    for month in ["01", "02", "03", "04", "05", "06", "08", "09", "10", "11", "12"]:
        print(month)

        for hour in range(0, 24):

            for days in range(0, 8):

                df_temp = df[
                    (df["month"] == month) & (df["hour"].astype(int) == hour) & (df["day"].astype(int) == days)]

                median = df_temp["Duration"].describe()[5]
                Q25 = df_temp["Duration"].describe()[4]
                Q75 = df_temp["Duration"].describe()[6]
                Q = Q75 - Q25
                wh_ = Q * 1.5
                upper = Q75 + wh_
                lower = Q25 - wh_
                if lower < 0:
                    lower = 0
                # print(upper, lower, wh_, median, Q, Q75,Q25)
                outlier_Ja_upper = df_temp[(df_temp["Duration"] > upper)]
                outlier_Ja_lower = df_temp[(df_temp["Duration"] < lower)]

                df_no_out = df_no_out.drop(outlier_Ja_upper.index)
                df_no_out = df_no_out.drop(outlier_Ja_lower.index)

        print(len(df_no_out))
        print(len(df))

    return df_no_out