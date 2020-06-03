import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
from ..io import read_file
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler
from tensorflow.keras.wrappers.scikit_learn import KerasRegressor
from geopy import distance as geo


def create_prediction_Duration(file):

    parse_dates = lambda x: dt.datetime.strftime(x, "%Y%M%D%H")

    # import the df, zipcode and the weather data
    df = read_file(file)
    weather = pd.read_csv(r"C:\Users\manue\git\PDS\Project\PDS_Project\data\frankfurt_weather_data2019.csv", sep=",",
                          index_col=0)
    zc = pd.read_csv(r"C:\Users\manue\git\PDS\Project\PDS_Project\geo_Data\backup_zipcodes.csv", index_col=0)

    # Take the basic df
    X_predictors = df

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

    # Create intervalls for hours
    X_predictors["hour"] = X_predictors["date"].astype(str).str.extract("([0-9]{2}$)")
    X_predictors["month"] = X_predictors["date"].str.replace("([0-9]{4}$)", "")

    # create month feature
    X_predictors["month"] = X_predictors["month"].astype(str).str.extract("([0-9]{2}$)")

    X_predictors["EVENING"] = ((X_predictors["hour"] > "18") | (X_predictors["hour"] == "00"))
    X_predictors["MIDDAY"] = ((X_predictors["hour"] > "12") & (X_predictors["hour"] <= "18"))
    X_predictors["MORNING"] = ((X_predictors["hour"] > "06") & (X_predictors["hour"] <= "12"))
    X_predictors["NIGHT"] = ((X_predictors["hour"] > "00") & (X_predictors["hour"] < "07"))

    X_predictors["EVENING"] = pd.to_numeric(X_predictors["EVENING"]).astype(int)
    X_predictors["MIDDAY"] = pd.to_numeric(X_predictors["MIDDAY"]).astype(int)
    X_predictors["MORNING"] = pd.to_numeric(X_predictors["MORNING"]).astype(int)
    X_predictors["NIGHT"] = pd.to_numeric(X_predictors["NIGHT"]).astype(int)

    location_Downtown = pd.DataFrame(data=[["point A", 8.683490753173828, 50.112817899138285]],
                                     columns=["Describtion", "long", "latitude"])

    # calculate durantion between center point of downtown and
    X_predictors["distan_Downtown"] = pd.Series(index=df.index, data=list(map(
        lambda x: geo.distance(tuple(location_Downtown.loc[0]["long":"latitude"]),
                               tuple((df.loc[x]["Start_Longitude"], df.loc[x]["Start_Latitude"]))).km, df.index)))

    # set temp to datetype string
    weather.index = weather.index.astype(str)

    # Join weather dates to predictor matrix
    X_predictors = X_predictors.join(weather, on="date", how="inner")

    # Set weekday from boolean to int
    X_predictors["Weekday"] = X_predictors["Weekday"].astype(int)

    # drop not needed weather data
    X_predictors.drop(columns=["relative humidity", "Rainfall", "SD_SO", "V_VV"], inplace=True)

    # get month as parameter
    month = pd.get_dummies(X_predictors["month"], drop_first=True)
    month.columns = ["FE", "MA", "AP", "MA", "JU", "AU", "SE", "OC", "NO", "DE"]
    X_predictors = X_predictors.join(month)

    # create dates
    start = dt.datetime(2019, 1, 20)
    dates = pd.date_range(start=start, end=dt.datetime(2019, 6, 30), periods=162)
    start = dt.datetime(2019, 8, 1)
    dates2 = pd.date_range(start=start, end=dt.datetime(2019, 12, 31), periods=153)
    dates = dates.append(dates2)
    dates

    median = pd.Series(index=dates, data=0)
    mean = pd.Series(index=dates, data=0)
    std = pd.Series(index=dates, data=0)

    count = 0
    for i in range(0, 315):
        start = dates[count]

        if i == 314:
            # median.loc[dates[count]] = df[(pd.to_datetime(df["Start_Time"]) >= dates[314])]["Duration"].describe()[4]
            mean.loc[dates[count]] = df[(pd.to_datetime(df["Start_Time"]) >= dates[314])]["Duration"].describe()[1]
            # std[dates[count]] = df[(pd.to_datetime(df["Start_Time"]) >= dates[314])]["Duration"].describe()[2]

            break;

        end = dates[count + 1]
        # median.loc[dates[count]] = df[(pd.to_datetime(df["Start_Time"]) >= start) & (pd.to_datetime(df["Start_Time"]) < end)]["Duration"].describe()[4]
        mean.loc[dates[count]] = \
        df[(pd.to_datetime(df["Start_Time"]) >= start) & (pd.to_datetime(df["Start_Time"]) < end)][
            "Duration"].describe()[1]
        # std[dates[count]] = df[(pd.to_datetime(df["Start_Time"]) >= start) & (pd.to_datetime(df["Start_Time"]) < end)]["Duration"].describe()[2]
        count += 1

    # format date for hour
    X_predictors["Start_Time_tem"] = pd.to_datetime(X_predictors["date"], format=("%Y%m%d%H"))
    hours = X_predictors.groupby("Start_Time_tem")["Duration"].mean()
    hours = pd.DataFrame(hours)
    count = 0

    # create the last hourly average
    for i in X_predictors.index:
        print(count)
        try:
            count += 1
            X_predictors.loc[i, "H1"] = hours.loc[X_predictors.loc[i, "Start_Time_tem"] - dt.timedelta(hours=1)][
                "Duration"]
            print(hours.loc[X_predictors.loc[i, "Start_Time_tem"] - dt.timedelta(hours=1)]["Duration"])
            X_predictors.loc[i, "H2"] = hours.loc[X_predictors.loc[i, "Start_Time_tem"] - dt.timedelta(hours=2)][
                "Duration"]
            X_predictors.loc[i, "H3"] = hours.loc[X_predictors.loc[i, "Start_Time_tem"] - dt.timedelta(hours=3)][
                "Duration"]
            X_predictors.loc[i, "H4"] = hours.loc[X_predictors.loc[i, "Start_Time_tem"] - dt.timedelta(hours=4)][
                "Duration"]
        except KeyError:
            print("null")

    # set the daily average of the last 2 days
    X_predictors["L1"] = pd.Series(index=df.index, data=list(
        map(lambda x: mean.shift(1)[pd.to_datetime(pd.to_datetime(df.loc[x]["Start_Time"]).strftime("%Y-%m-%d"))],
            df.index)))
    X_predictors["L2"] = pd.Series(index=df.index, data=list(
        map(lambda x: mean.shift(2)[pd.to_datetime(pd.to_datetime(df.loc[x]["Start_Time"]).strftime("%Y-%m-%d"))],
            df.index)))

    #
    X_predictors["L1"].fillna(value=0, inplace=True)
    X_predictors["L2"].fillna(value=0, inplace=True)
    X_predictors["H1"].fillna(value=0, inplace=True)
    X_predictors["H2"].fillna(value=0, inplace=True)
    X_predictors["H3"].fillna(value=0, inplace=True)
    X_predictors["H4"].fillna(value=0, inplace=True)

    # Set target to Y (durations)
    Y = pd.DataFrame(columns=["Duration"], data=X_predictors["Duration"])

    # Drop duration from predictor
    X_predictors.drop(
        columns=["month", "Start_Time", "Duration", "hour", "date", "Zip_codes", "Start_Time_tem", "Duration_log"],
        inplace=True)

    X_predictors

    return X_predictors, Y


def create_predictors_classification(file):
    df = read_file(file)
    location_Uni = pd.DataFrame(data=[["point A", 7.667011260986328, 50.12687889430692]],
                                columns=["Describtion", "long", "latitude"])

    # calculate durantion between center point of univer. and trip end classifi
    distance = df[list(map(lambda x: 0.0 >= geo.distance(tuple(location_Uni.loc[0]["long":"latitude"]), tuple(
        (df.loc[x]["End_Longitude"], df.loc[x]["End_Latitude"]))).km, df.index))]
    distance["uni"] = 0
    df["To_Uni"] = -1
    df["To_Uni"] = pd.Series(distance["uni"])
    df["To_Uni"].fillna(value=-1, inplace=True)

    # create feature lecture time or no lecture time
    df["Lecture_Time"] = False

    # check if trip is lecture free time
    lecture = df[list(map(
        lambda x: (df.loc[x]["Start_Time"] > "2018-04-15 00:00:00") & (df.loc[x]["Start_Time"] < "2019-09-20 00:00:00"),
        df.index))]
    lecture["Lecture_Time"] = 0

    # set number
    pd.to_numeric(df["Lecture_Time"])
    df["Lecture_Time"] = pd.Series(lecture["Lecture_Time"])
    df["Lecture_Time"].fillna(value=-1, inplace=True)

    # create hour feature
    df["date"] = df["Start_Time"].astype(str).str.replace("-", "")
    df["date"] = df["date"].str.replace(":*:.*", "")
    df["date"] = df["date"].str.replace("\s", "")

    # Create intervalls for hours
    df["hour"] = df["date"].astype(str).str.extract("([-1-9]{2}$)")

    # Create intervalls for hours
    df["month"] = df["Start_Time"].astype(str).str.extract("(-[-1-9]{2}-)")
    print(df["month"])
    df["month"] = df["month"].astype(str).str.replace("-", "")
    print(df["month"])
    #create dummies for month
    month = pd.get_dummies(df["month"], drop_first=True)
    print(month)
    month.columns = ["FE", "MA", "AP", "MA", "JU", "AU", "SE", "OC", "NO", "DE"]

    df.drop(columns=["month"])
    # drop not needed columns
    df = df.drop(columns=['month', 'Duration', 'End_Longitude', 'Zip_codes', 'Bike_number', 'Start_Time', 'End_time',
                          'Start_Station', 'End_Latitude', 'date', 'hour', 'Bikes_on_position', 'End_Station_number',
                          'End_Bikes'])
    data = pd.concat([df, month], axis=0)

    # set target
    target_vector = data["To_Uni"]

    # drop target from predictors
    data.drop(columns=["To_Uni"], inplace=True)
    pred_matrix = data

    return pred_matrix, target_vector
