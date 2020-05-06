import pandas as pd
import numpy as np
import datetime as dt
from .input import read_file


def create_df(base):

    base.isnull().any()
    base["datetime"] = pd.to_datetime(base["datetime"], format="%Y-%m-%d %H:%M:%S")

    # read all data that contains trips from data set
    base_trips = base[(base["trip"].str.contains("(start|end)"))]

    base["p_number"].value_counts()

    # sort the values of the df
    base_trips = pd.DataFrame(base_trips.sort_values(by=['b_number', 'datetime']), index=None).reset_index()

    # drop index column
    base_trips.drop(["index"], axis=1, inplace=True)
    base_trips

    # Find the start bookings in data set
    start_rows = base_trips[list(map(lambda x: base_trips.loc[x]["trip"] == "start", base_trips.index))]
    end_rows = base_trips[list(map(lambda x: base_trips.loc[x]["trip"] == "end", base_trips.index))]

    # Filter double starts or ends for same bike
    wrong_starts = pd.Series(list(filter(lambda x: False if (x == 0) else base_trips.loc[int(x-1)]["trip"] == "start",
                                         start_rows.index)))

    wrong_ends = pd.Series(list(filter(lambda y: False if (y == end_rows.index[-1]) else base_trips.loc[int(y+1)]["trip"] == "end",
                                       end_rows.index)))

    # Append Index to delete to one list
    if wrong_ends.empty:
        wrong_series = pd.Series(wrong_starts)
    else:
        wrong_series = pd.Series(wrong_starts.append(wrong_ends))
    print(wrong_starts)

    # drop redundant id start and reset index to get right index shift
    base_trips.drop(wrong_series, axis=0, inplace=True)
    base_trips.reset_index(inplace=True)
    base_trips.drop("index", axis=1, inplace=True)

    # created new rows for start because of reindexing
    start_rows_new = base_trips[list(map(lambda x: base_trips.loc[x]["trip"] == "start", base_trips.index))]
    end_rows_new = base_trips[list(map(lambda y: base_trips.loc[y]["trip"] == "end", base_trips.index))]

    print(start_rows_new, end_rows_new)

    # Select every start that has a end booking in data (data set already sort with bike number and datetime)
    starts_has_end = list(filter(lambda x: base_trips.loc[x + 1]["trip"] == "end", start_rows_new.index))

    # created temp df
    start_trips = base_trips.iloc[starts_has_end]

    # calculate duration
    durations = list(map(lambda x: end_rows_new.iloc[x]["datetime"] - start_rows_new.iloc[x]["datetime"],
                         range(0, len(start_rows_new))))

    # create the new data frame for analysis, rename columns added new columns
    trip_wduration = pd.DataFrame(start_trips.rename(columns={"b_number": "Bike_number", "p_lat": "Start_Latitude",
                                                              "p_lng": "Start_Longitude", "p_spot": "Station_position",
                                                              "datetime": "Starttime", "p_place_type": "Type_of_Place",
                                                              "p_spot": "Station_position", "p_bike": "Bike_position",
                                                              "p_number": "Station_number",
                                                              "p_uid": "Start_position_UID",
                                                              "p_bikes": "Bikes_on_position",
                                                              "b_bike_type": "Bikes_type"}))

    # Calculate if booking is on weekday
    print(trip_wduration)
    weekday = list(map(lambda x: trip_wduration.loc[x]["Starttime"].weekday() < 5, trip_wduration.index))

    trip_wduration.drop(["trip", "p_name"], axis=1, inplace=True)
    trip_wduration["duration"] = durations
    trip_wduration["weekday"] = weekday
    trip_wduration["Bike_number"] = start_trips["b_number"]

    trip_wduration["Endtime"] = trip_wduration["Starttime"] + (pd.to_timedelta(trip_wduration["duration"]))
    trip_wduration["End_position_UID"] = pd.Series(index=trip_wduration.index, data=end_rows_new["p_uid"].values)
    trip_wduration["End_Latitude"] = pd.Series(index=trip_wduration.index, data=end_rows_new["p_lat"].values)
    trip_wduration["End_Longitude"] = pd.Series(index=trip_wduration.index, data=end_rows_new["p_lng"].values)

    return trip_wduration


# method to perform cleaning data frame from wrong data.
def clean_df(df):

    df = pd.DataFrame(df)
    missingi_data_frame = df[df["place"]]
    short_trip = df[(df["duration"] <= dt.timedelta(minutes=3)) & (df["End_position_UID"] == df["Start_position_UID"])]
    # drop short values from data frame
    df.drop(short_trip.index, inplace=True)
