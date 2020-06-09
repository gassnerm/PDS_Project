import os

import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
from ..io import read_file, get_data_path, set_data_frame
from geopy import distance as geo


# training flag to define if the call is for training to drop ether the training or the test set
def create_prediction_Duration(file, trainingflag):

    # parse date to date time
    parse_dates = lambda x: dt.datetime.strftime(x, "%Y%M%D%H")

    # import the df, zipcode and the weather data
    df = file

    # append test set for features
    weather = read_file("frankfurt_weather_data2019.csv")
    zc = read_file(r"..\geo_Data\backup_zipcodes.csv")

    # make a data frame for weather data
    weather = pd.DataFrame(weather)

    # create the data frame for zip codes
    zc = pd.DataFrame(zc)

    # Take the basic df
    X_predictors = df

    print("Drop unneeded columns")
    # Create the predictor matrix columns that are not needed
    X_predictors = X_predictors.drop(columns=["Start_Latitude"
        , "Bike_number"
        , "Start_Longitude"
        , "End_Station_number"
        , "End_time"
        , "End_Latitude"
        , "End_Longitude"
        , "Bikes_on_position"
        , "End_Bikes", "Start_Station"])

    # Format date to other format "2019-20-01 00:00:00 to 2019200100"
    X_predictors["date"] = X_predictors["Start_Time"].astype(str).str.replace("-", "")
    X_predictors["date"] = X_predictors["date"].str.replace(":*:.*", "")
    X_predictors["date"] = X_predictors["date"].str.replace("\s", "")

    # Use zip code for border districts
    X_predictors["Borderdistrict"] = X_predictors["Zip_codes"].isin([65929, 60529, 60549, 65931, 65936, 60528, 60388, 60437, 60438, 60439,
                                                 60433, 60598, 60599, 63067, 60314, 60386]).astype(int)


    # Create intervalls for hours
    X_predictors["hour"] = X_predictors["date"].astype(str).str.extract("([0-9]{2}$)")
    X_predictors["month"] = X_predictors["date"].str.replace("([0-9]{4}$)", "")

    # create month feature
    X_predictors["month"] = X_predictors["month"].astype(str).str.extract("([0-9]{2}$)")

    # create time buckets
    X_predictors["EVENING"] = ((X_predictors["hour"] > "18") | (X_predictors["hour"] == "00"))
    X_predictors["MIDDAY"] = ((X_predictors["hour"] > "12") & (X_predictors["hour"] <= "18"))
    X_predictors["MORNING"] = ((X_predictors["hour"] > "06") & (X_predictors["hour"] <= "12"))
    X_predictors["NIGHT"] = ((X_predictors["hour"] > "00") & (X_predictors["hour"] < "07"))
    X_predictors["EVENING"] = pd.to_numeric(X_predictors["EVENING"]).astype(int)
    X_predictors["MIDDAY"] = pd.to_numeric(X_predictors["MIDDAY"]).astype(int)
    X_predictors["MORNING"] = pd.to_numeric(X_predictors["MORNING"]).astype(int)
    X_predictors["NIGHT"] = pd.to_numeric(X_predictors["NIGHT"]).astype(int)

    # format date for hour
    X_predictors["Start_Time_tem"] = pd.to_datetime(X_predictors["date"], format=("%Y%m%d%H"))
    X_predictors["Duration"] = X_predictors["Duration"].astype(float)
    hours = X_predictors.groupby("Start_Time_tem")["Duration"].mean()
    hours = pd.DataFrame(hours)
    count = 0

    print("Start")
    # create the hourly averages of the last 7 hours before booking
    for i in X_predictors.index:

        try:
            count += 1
            X_predictors.loc[i, "H1"] = hours.loc[X_predictors.loc[i, "Start_Time_tem"] - dt.timedelta(hours=1)][
                "Duration"]
        except KeyError:
            continue
        try:
            X_predictors.loc[i, "H2"] = hours.loc[X_predictors.loc[i, "Start_Time_tem"] - dt.timedelta(hours=2)][
                "Duration"]
        except KeyError:
            continue
        try:
            X_predictors.loc[i, "H3"] = hours.loc[X_predictors.loc[i, "Start_Time_tem"] - dt.timedelta(hours=3)][
                "Duration"]
        except KeyError:
            continue
        try:
            X_predictors.loc[i, "H4"] = hours.loc[X_predictors.loc[i, "Start_Time_tem"] - dt.timedelta(hours=4)][
                "Duration"]
        except KeyError:
            continue
    print("end")


    # set temp to datetype string
    weather.index = weather.index.astype(str)

    # Join weather dates to predictor matrix
    X_predictors = X_predictors.join(weather, on="date", how="inner")

    # Set weekday from boolean to int
    X_predictors["Weekday"] = X_predictors["Weekday"].astype(bool)
    X_predictors["Weekday"] = X_predictors["Weekday"].astype(int)

    # drop not needed weather data
    X_predictors.drop(columns=["relative humidity", "Rainfall", "SD_SO", "V_VV"], inplace=True)


    # get month as parameter
    #month = pd.get_dummies(X_predictors["month"], drop_first=True)
    #month.columns = ["FE", "MA", "AP", "MA", "JU", "AU", "SE", "OC", "NO", "DE"]
    #X_predictors = X_predictors.join(month)

    # create dates for weekly average
    start = dt.datetime(2019, 1, 20)
    dates = pd.date_range(start=start, end=dt.datetime(2019, 12, 31), periods=346)
    dates


    # set mean series
    mean = pd.Series(index=dates, data=0)

    count = 0

    # create dates for each day in the data set
    for i in range(0, 346):

        # calculate average duration for each day
        start = dates[count]
        if i == 345:

                # calculate the mean for day
                mean.loc[dates[count]] = df[(pd.to_datetime(df["Start_Time"]) >= dates[345])]["Duration"].describe()[1]
                break
        # calculate the mean for days
        end = dates[count + 1]
        mean.loc[dates[count]] = df[(pd.to_datetime(df["Start_Time"]) >= start) & (pd.to_datetime(df["Start_Time"]) < end)]["Duration"].describe()[1]
        count += 1
    print("Dates series: ", dates)


    # calculated hourly mean for duration
    X_predictors["L1"] = pd.Series(index=df.index, data=list(map(lambda x: mean.shift(1)[pd.to_datetime(pd.to_datetime(df.loc[x]["Start_Time"]).strftime("%Y-%m-%d"))], df.index)))
    X_predictors["L2"] = pd.Series(index=df.index, data=list(map(lambda x: mean.shift(2)[pd.to_datetime(pd.to_datetime(df.loc[x]["Start_Time"]).strftime("%Y-%m-%d"))], df.index)))

    # fill null values, no future information
    X_predictors.fillna(value=0, inplace=True)


    # round every value to 3 decimal
    df = df.round(3)

    # if model is trained drop test set after feature creation for predict drop train set
    if trainingflag:
        # drop test set
        X_predictors = X_predictors[X_predictors["month"] != "07"]
    else:
        # drop test set
        X_predictors = X_predictors[X_predictors["month"] == "07"]


    # Set target to Y (durations)
    Y = pd.DataFrame(columns=["Duration"], data=X_predictors["Duration"])


    # Drop duration from predictor
    X_predictors.drop(
        columns=["month", "Start_Time", "Duration", "hour", "date", "Zip_codes", "Start_Time_tem"],
        inplace=True)

    print("fill null values")
    # fill na values
    X_predictors.fillna(value=0, inplace=True)

    print("Feature creation finished")
    return X_predictors, Y


# training flag to define if the call is for training to drop ether the training or the test set
def create_predictors_classification(file, training_Flag):

    # set data frame and reset index duplicated index
    # in df because previes append
    df = file
    df.reset_index(inplace=True, drop=True)

    print(len(df))
    weather = read_file(r"frankfurt_weather_data2019.csv")
    weather = pd.DataFrame(weather)

    # load start location of the university of applied science
    location_Uni = pd.DataFrame(data=[["point A", 8.692339207868319, 50.130519449999994]],
                                columns=["Describtion", "long", "latitude"])

    #df = df[38000:]
    # calculate durantion between center point of univer. and trip end classifi
    distance_begin = pd.Series(index=df.index, data=list(map(
        lambda x: geo.distance(tuple(location_Uni.loc[0]["long":"latitude"]),
                               tuple((df.loc[x]["Start_Longitude"], df.loc[x]["Start_Latitude"]))).km, df.index)))
    distance_end = pd.Series(index=df.index, data=list(map(
        lambda x: geo.distance(tuple(location_Uni.loc[0]["long":"latitude"]),
                               tuple((df.loc[x]["End_Longitude"], df.loc[x]["End_Latitude"]))).km, df.index)))

    Dist = pd.DataFrame(distance_begin)

    # Create target column
    Dist["end_d"] = distance_end
    Dist["uni"] = Dist[0] > Dist["end_d"]
    Dist["uni"] = Dist["uni"].astype(int)
    df = Dist.join(df)

    df["weather"] = 0

    # stardistanz, hour, month,
    df["date"] = df["Start_Time"].astype(str).str.replace("-", "")
    df["date"] = df["date"].str.replace(":*:.*", "")
    df["date"] = df["date"].str.replace("\s", "")


    # set temp to datetype string
    weather.index = weather.index.astype(str)

    # Join weather dates to predictor matrix
    df = df.join(weather, on="date", how="inner")

    # set weather condition
    df["weather"] = (df["hourly temperatur"].astype(float) > 5) & (df["Rainfall"].astype(float) == 0)
    df.drop(columns=["relative humidity", "Rainfall", "SD_SO", "V_VV"], inplace=True)
    df["weather"] = df["weather"].astype(int)

    # Create intervalls for hours
    df["hour"] = df["date"].astype(str).str.extract("([0-9]{2}$)").astype(int)

    # exctract month
    df["month"] = df["date"].astype(str).str.extract("(^[0-9]{6})").astype(int)
    df["month"] = df["month"].astype(str).str.extract("([0-9]{2}$)").astype(int)

    # create zip code feature for border quarter and student quarters
    df["Borderdistrict"] = df["Zip_codes"].isin([65929, 60529, 60549, 65931, 65936, 60528, 60388, 60437, 60438, 60439,
                                                 60433, 60598, 60599, 63067, 60314, 60386])
    df["Student_quarter"] = df["Zip_codes"].isin([60385, 60487, 60385, 60326, 60486, 6028, 60327, 60488, 60487, 65929])

    # Set values to int
    df["Student_quarter"] = df["Student_quarter"].astype(int)
    df["Borderdistrict"] = df["Borderdistrict"].astype(int)
    df["Weekday"] = df["Weekday"].astype(int)






    # get all zip codes
    zipcodes = df["Zip_codes"].value_counts()

    # creat week number
    df["week"] = pd.to_datetime(df["Start_Time"]).dt.strftime('%W').astype(int)

    # generate feature for zip codes pro.
    for plz in zipcodes.index:
        for i in range(0, 52):
            value = df[(df["uni"] == 1) & (df["Zip_codes"] == plz) & (df["week"] < i)]["uni"].count()
            value = value / (df[(df["Zip_codes"] == plz) & (df["week"] < i)])["uni"].count()
            df.loc[df[(df["Zip_codes"] == plz) & (df["week"] == i)].index, "zip_pro"] = value
    df["zip_pro"].value_counts(bins=20)

    # get pro. that station start will go towards university based on start information
    Start_Station = df["Start_Station"].value_counts()
    for std in Start_Station.index:
        for w in range(0, 52):
            value = df[(df["uni"] == 1) & (df["Start_Station"] == std) & (df["week"] < w)]["uni"].count()
            value = value / (df[(df["Start_Station"] == std) & (df["week"] < w)])["uni"].count()
            df.loc[df[(df["Start_Station"] == std) & (df["week"] == w)].index, "Start_Station_pro"] = value




    if training_Flag:
        # drop test set
        df = df[df["month"] != 7]
    else:
        # drop test set
        df = df[df["month"] == 7]


    # set target values
    target_vector = df["uni"]


    # Drop target from predictor
    df.drop(columns=["uni"], inplace=True)



    print(df)

    # drop columns not needed
    df.drop(columns=["month","hourly temperatur","Zip_codes", "Start_Station", "Start_Time", "Start_Longitude", "Start_Latitude",
                     "end_d", "date", "End_Bikes", "Bike_number", "End_time", "End_Longitude", "End_Latitude",
                     "End_Station_number", "Duration", "Bikes_on_position", "hour","week"], inplace=True)
    df = df.round(3)
    print(df.isnull().any())
    df.fillna(value=0, inplace=True)
    # set predictor matrix
    pred_matrix = df

    # return predictor matrix and target vector
    return pred_matrix, target_vector
