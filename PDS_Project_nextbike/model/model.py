import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.preprocessing import RobustScaler, PolynomialFeatures
from sklearn.preprocessing import StandardScaler
from ..io import save_model
import pandas as pd


from sklearn.decomposition import PCA

# trains the regression algorithm
def train_prediction_duration(X_duration, Y_duration, d):

    X_duration = X_duration.to_numpy()
    Y_duration = Y_duration.to_numpy()

    # set test, train set split apply log tarnsformation
    X_train, X_test, y_train, y_test = train_test_split(X_duration, np.log(Y_duration), test_size=0.3)

    # use log transformation
    Y_duration = np.log(Y_duration)

    # determine the degree of the regression
    poly_reg = PolynomialFeatures(degree=d)

    # Create polynomial features for the 15 predictors fit transform no scaler needed
    x_poly_matrix = poly_reg.fit_transform(X_duration.reshape(-1, 23))

    # Fitting linear regression to polynomial features that are created
    lin_reg_Poly = LinearRegression()
    lin_reg_Poly.fit(x_poly_matrix, Y_duration)

    # save the model to data folder
    save_model(lin_reg_Poly, False)


def train_nn_classification_task(x, y):
    # set to array
    x = x.to_numpy()
    y = y.to_numpy()
    # splitting predictor and target
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

    st_scaler = StandardScaler()
    st_scaler.fit(x_train)
    X_train_scaled = st_scaler.transform(x_train)


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

    # set parameter for nn epochs and batch size
    epochs = 20
    batch_size = 5000


    # create the model history and fit the model
    model.fit(X_train_scaled, y_train, batch_size=batch_size, epochs=epochs, validation_split=0.2)

    save_model(model, True)

    # return test set and the history epos
    return x_test, y_test


