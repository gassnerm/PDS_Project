from tensorflow_core.python.keras.wrappers.scikit_learn import KerasClassifier

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
from .create_predictors import create_predictors_classification, create_prediction_Duration




def train():


    lin = LinearRegression()
    print("Linear model created")
    print("Training...")

    io.save_model(lin)


def train_nn_classification_task(df_file):
    # get predictor and target
    x, y = create_predictors_classification(df_file)
    print("split data set in test and train set")
    # splitting predictor and target
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

    # stand. the training set
    st_scaler = StandardScaler()
    st_scaler.fit(x_train)

    # set parameter for nn epochs and batch size
    epochs = 50
    batch_size = 500

    # outliner haneling use Robust scaler
    scaler = RobustScaler()

    # create nn object with parameters
    nn = KerasClassifier(NNClassifier(x_train), epochs=epochs, batch_size=batch_size, validation_split=0.2)

    # use polynomial features
    poly = PolynomialFeatures

    # creating pipeline with scaler, nn and polynomial features
    pipe = Pipeline([
        ("poly", poly)
        ("Robust Scaler", scaler),  # fit -> transform
        ("Neural Network", nn)  # fit
    ])
    param_grid = {
            # starting pol before scale for ensure of magnitude for pol features and then scale it
            'poly__degree': [1, 2],
            'nn__dropout_rate': [0.5]
        }
    grid = GridSearchCV(pipe, param_grid, cv=5, verbose=True, n_jobs=4, scoring="neg_root_mean_squared_error")

    # fit training set
    grid.fit(x_train, y_train)

    # get reports from pipeline
    grid_df = pd.DataFrame(grid.cv_results_["params"])
    grid_df["loss"] = -grid.cv_results_["mean_test_score"]
    grid_df

    # predict the test set
    y_pred = pipe.predict(x_test)

    from matplotlib.colors import LogNorm

    fig, ax = plt.subplots(1,1, figsize=(3, 3), dpi=100)
    sns.heatmap(grid_df.pivot(columns="nn__dropout_rate", values="loss", index="poly__degree"), cmap=coolwarm, ax=ax)
    ax.set_title("Grid Search Hyperparameter")


# create classifier for nn
def NNClassifier(x_train):
    model = keras.Sequential(
        [layers.Dense(50, activation="sigmoid", input_shape=[x_train.shape[1]]),
         layers.Dropout(0.2),
         layers.Dense(50, activation="sigmoid", ),
         layers.Dropout(0.2),
         layers.Dense(50, activation="sigmoid"),
         layers.Dropout(0.2),
         layers.Dense(1)])

    optimizer = keras.optimizers.Adam()

    model.compile(loss='mse',
                  optimizer=optimizer,
                  metrics=["mae"])
    return model
