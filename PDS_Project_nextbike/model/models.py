import numpy as np
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.preprocessing import RobustScaler, PolynomialFeatures
from sklearn.preprocessing import StandardScaler
from ..io import save_model
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


# trains the regression algorithm
def train_prediction_duration(X_duration, Y_duration):

    columns = np.array(X_duration.columns).reshape(13,1)
    X_duration = X_duration.to_numpy()
    Y_duration = Y_duration.to_numpy()

    # use log transformation
    Y_duration = np.log(Y_duration)

    st_scaler = StandardScaler()
    st_scaler.fit(X_duration)
    X_train_scaled = st_scaler.transform(X_duration)


    # Fitting linear regression to polynomial features that are created
    lin_reg = LinearRegression()
    lin_reg.fit(X_train_scaled, Y_duration)

    print(" Coeffient", pd.DataFrame(lin_reg.coef_.T, index=[ "Weekday", "Borderdistrict",  "EVENING",  "MIDDAY",
                                                            "MORNING","NIGHT","H1","H2","H3","H4","hourly temperatur"
                                                            ,"L1","L2"], columns=["Coefficient"]))
    print("intercept: ", lin_reg.intercept_)
    # save the model to data folder
    save_model(lin_reg, False)


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
            [layers.Dense(17, activation="sigmoid", input_shape=[x_train.shape[1]]),
            layers.Dropout(0.1),
            layers.Dense(17, activation="sigmoid", ),
            layers.Dropout(0.1),
            layers.Dense(17, activation="sigmoid", ),
            layers.Dropout(0.1),
            layers.Dense(17, activation="sigmoid", ),
            layers.Dropout(0.1),
            layers.Dense(1)])

    optimizer = keras.optimizers.Adam(learning_rate=0.01)

    model.compile(loss='rmse',
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

