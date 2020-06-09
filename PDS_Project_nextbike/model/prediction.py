from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn import metrics
import pandas as pd
from ..io import read_model, plt, write_file, read_scaler
import numpy as np
from tensorflow import keras
import os
import seaborn as sns
from  sklearn.metrics import accuracy_score



def create_duration_prediction(X_test, y_test):


    # set to array
    X_test = X_test.to_numpy()
    y_test = y_test.to_numpy()

    # use log transformation
    y_test = np.log(y_test)

    # import the models for regression
    lin = read_model(False)

    st_scaler = read_scaler(False)


    X_test_scaled = st_scaler.transform(X_test)

    # prediction of test set by trained model log transform
    model_pre_test = lin.predict(X_test_scaled)


    print(model_pre_test.shape, y_test.shape)

    # back transform the ylog transformed values
    print("RMSE: ", np.sqrt(metrics.mean_squared_error(y_test, np.exp(model_pre_test))))
    print("MAE: ", metrics.mean_absolute_error(y_test, np.exp(model_pre_test)))
    print("r²: ", metrics.r2_score(y_test, model_pre_test))


    plt.scatter(model_pre_test, y_test)

    # transform data back to normal scale
    write_file("prediction_duration.csv",  model_pre_test)


def create_classification_prediction(X, Y):

    # read saved model
    model = keras.models.load_model(os.getcwd() + r"\output_data\classif_model.h5")



    st_scaler = read_scaler(True)

    st_scaler.fit(X)

    # scale predictors
    X_test_scaled = st_scaler.transform(X)

    # predict given test set
    y_pred = model.predict(X_test_scaled)


    # get the metrics for the test set
    print(accuracy_score(Y, y_pred.round()))
    print(confusion_matrix(Y, y_pred.round()))
    write_file("prediction_classif.csv",  y_pred)


