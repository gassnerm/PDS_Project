import pandas as pd
import numpy as np
import datetime as dt
from .input import read_file
from .utils import *
from .createStatisics import create_statistics


def create_df(base):

    # drop na values and wrong data
    base = pd.DataFrame(clean_df(base))
    print("Raw DF :", base)

    # parse string series datetime to datetime
    base["datetime"] = pd.to_datetime(base["datetime"], format="%Y-%m-%d %H:%M:%S")

    # read all data that contains trips from data set drop all first and last rows
    base_trips = base[(base["trip"].str.contains("(start|end)"))]
    print("Without first and last:", base_trips)

    # sort the values of the df
    base_trips = pd.DataFrame(base_trips.sort_values(by=['b_number', 'datetime']), index=None).reset_index(drop=True)

    # Find the start and end bookings in data set
    start_rows = base_trips[base_trips["trip"] == "start"]
    end_rows = base_trips[base_trips["trip"] == "end"]
    # Filter double starts or ends for same bike

    wrong_starts = pd.Series((base_trips[base_trips['trip'] == base_trips['trip'].shift(-1)]["trip"]))

    # drop redundant id start and reset index to get right index shift
    base_trips.drop(wrong_starts.index, axis=0, inplace=True)
    print("After dropping doppel starts and ends ", base_trips)
    base_trips.reset_index(inplace=True, drop=True)

    # created new rows for start because of reindexing
    start_rows_new = base_trips[base_trips["trip"] == "start"].reset_index(drop=True)
    end_rows_new = base_trips[base_trips["trip"] == "end"].reset_index(drop=True)

    # Select every start that has a end booking in data (data set already sort with bike number and datetime)
    # starts_has_end = list(filter(lambda x: base_trips.loc[x + 1]["trip"] == "end", start_rows_new.index))

    starts_has_end = start_rows_new[(start_rows_new["b_number"] == end_rows_new["b_number"]) & (start_rows_new["datetime"] < end_rows_new["datetime"])]


    # created temp df
    # start_trips = base_trips.iloc[starts_has_end.index]
    print("Trips that has a end ", starts_has_end)

    # calculate duration
    durations = pd.Series(end_rows_new["datetime"] - start_rows_new["datetime"])

    # create the new data frame for analysis, rename columns added new columns
    trip_wduration = pd.DataFrame(starts_has_end.rename(columns={"p_name": "Start_Place", "b_number": "Bike_number",
                                                              "p_lat": "Start_Latitude",
                                                              "p_lng": "Start_Longitude",
                                                              "p_spot": "Start_Station_position",
                                                              "datetime": "Start_Time",
                                                              "p_spot": "Station_position",
                                                              "p_bike": "Bike_position",
                                                              "p_number": "Start_Station",
                                                              "p_uid": "Start_position_UID",
                                                              "p_bikes": "Bikes_on_position"
                                                              }))

    # Calculate if booking is on weekday
    print(trip_wduration)
    weekday = (pd.DatetimeIndex(trip_wduration["Start_Time"]).dayofweek < 5)


    trip_wduration["Duration"] = pd.Series(index=trip_wduration.index, data=cast_timedelta_to_number(durations).values)
    trip_wduration["Duration"] = trip_wduration["Duration"]
    trip_wduration["Weekday"] = weekday
    trip_wduration["Bike_number"] = starts_has_end["b_number"]
    trip_wduration["End_Station_position"] = pd.Series(index=trip_wduration.index, data=end_rows_new["p_spot"].values)
    trip_wduration["End_time"] = pd.Series(index=trip_wduration.index, data=end_rows_new["datetime"].values)
    trip_wduration["End_position_UID"] = pd.Series(index=trip_wduration.index, data=end_rows_new["p_uid"].values)
    trip_wduration["End_Latitude"] = pd.Series(index=trip_wduration.index, data=end_rows_new["p_lat"].values)
    trip_wduration["End_Longitude"] = pd.Series(index=trip_wduration.index, data=end_rows_new["p_lng"].values)
    trip_wduration["End_Station_number"] = pd.Series(index=trip_wduration.index, data=end_rows_new["p_number"].values)

    # drop trips that are shorter or 3 minutes long and did n change location
    trip_wduration = drop_short_long_trips(trip_wduration)
    print("Drop to short trips ", trip_wduration)

    # Drop negative coordinates
    trip_wduration = cleaning_new_df(trip_wduration)
    print("Drop negative coorindinates ", trip_wduration["Duration"].count())

    # read geo data
    geo_data = read_file("data/backup_zipcodes.csv")

    # create the zip code column for trips
    trip_wduration = create_zip_code_data(trip_wduration, geo_data)
    print("Zip_codes ", trip_wduration["Duration"].count())

    # drop columns used to join the geo_data
    trip_wduration.drop(labels="Coordinates", axis=1, inplace=True)

    # drop columns based on box plot whiskers
    # trip_wduration = drop_outlier(trip_wduration)

    # drop not needed columns
    trip_wduration.drop(["trip", "p_place_type", "b_bike_type", "Start_position_UID", "Station_position",
                         "Start_Place", "Bike_position", "End_position_UID", "End_Station_position"], axis=1, inplace=True)

    # Set schedule for columns
    cols = trip_wduration.columns.tolist()
    cols = cols[1:2] + cols[0:1] + cols[3:4] + cols[5:6] + cols[4:5] + cols[7:8] + cols[9:10] + cols[10:11] + cols[6:7] + \
           cols[-2:-1] + cols[-1:] + cols[2:3]

    trip_wduration = trip_wduration[cols]

    print("Finish", trip_wduration)
    return trip_wduration



