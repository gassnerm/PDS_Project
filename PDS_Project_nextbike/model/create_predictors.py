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


def create_prediction_Duration():
    df = pd.read_csv(r"/output_data/transform_DF", index_col=0)

    df_mapping = pd.Series({0: "Monday",
                        1: "Tuesday",
                        2: "Wednesday",
                        3: "Thurday",
                        4: "Friday",
                        5: "Saturday",
                        6: "Sunday"})


    holiday_winter = dt.datetime(2019, 1, 12)
    holiday_spring = dt.datetime(2019, 4, 27)
    holiday_sommer = dt.datetime(2019, 8, 9)
    holiday_fall = dt.datetime(2019, 10, 12)
    holiday_crism = dt.datetime(2019, 12, 31)


    date_list = pd.Series([str(holiday_winter - dt.timedelta(days=x)) for x in range(0,12)], dtype=str)
    date_list2 = pd.Series([str(holiday_spring - dt.timedelta(days=x)) for x in range(0,12)], dtype=str)
    date_list3 = pd.Series([str(holiday_sommer - dt.timedelta(days=x)) for x in range(0,40)], dtype=str)
    date_list4 = pd.Series([str(holiday_fall - dt.timedelta(days=x)) for x in range(0,13)], dtype=str)
    date_list5 = pd.Series([str(holiday_crism - dt.timedelta(days=x)) for x in range(0,9)], dtype=str)

    date_list = date_list.append(date_list2, ignore_index=False).reset_index(drop = True)
    date_list = date_list.append(date_list3, ignore_index=False).reset_index(drop = True)
    date_list = date_list.append(date_list4, ignore_index=False).reset_index(drop = True)
    date_list = date_list.append(date_list5, ignore_index=False).reset_index(drop = True)


    df_holiday = pd.Series({0: "2019-05-01",
                            1: "2019-05-30",
                            2: "2019-06-10",
                            3: "2019-06-20"})

    df_holiday = df_holiday.append(date_list.astype(str)).reset_index(drop=True)
    df_holiday = pd.Series(index=df_holiday.index, data=list(map(lambda x: str(x[0:10]), df_holiday.values)))


    df["day"] = pd.Series(index=df.index,data=list(map(lambda x: df_mapping[int(pd.to_datetime(str(x)).weekday())], df["Starttime"])))

    df["hour"] = pd.Series(index=df.index, data=list(map(lambda x: str(df.loc[x]["Starttime"])[11:13], df.index)))

    df["holiday"] = pd.Series(index=df.index, data=list(map(lambda x: df.loc[x]["Starttime"][0:10] in df_holiday.values, df.index)))


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
