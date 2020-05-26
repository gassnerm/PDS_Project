from .. import io
from ..io import read_file
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, PolynomialFeatures, RobustScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import Ridge, Lasso
from sklearn.pipeline import Pipeline
from sklearn import metrics
#Import for project
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
#Import for project
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler
from tensorflow.keras.wrappers.scikit_learn import KerasRegressor
from geopy import distance as geo





def train():


    lin = LinearRegression()
    print("Linear model created")
    print("Training...")

    io.save_model(lin)


def classification_Task():
    # load data set
    df = read_file("transform_DF", index_col=0)

    location_Uni = pd.DataFrame(data=[["point A", 8.667011260986328, 50.12687889430692]],
                                columns=["Describtion", "long", "latitude"])

    # calculate durantion between center point of univer. and trip end classifi
    distance = df[list(map(lambda x: 1.0 >= geo.distance(tuple(location_Uni.loc[0]["long":"latitude"]), tuple(
        (df.loc[x]["End_Longitude"], df.loc[x]["End_Latitude"]))).km, df.index))]
    distance["uni"] = 1
    df["To_Uni"] = 0
    df["To_Uni"] = pd.Series(distance["uni"])
    df["To_Uni"].fillna(value=0, inplace=True)



