from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn import metrics
import pandas as pd
from ..io import read_model, plt, write_file
import numpy as np
from tensorflow import keras
import os


def create_duration_prediction(X_test, y_test):

    # set to array
    X_test = X_test.to_numpy()
    y_test = y_test.to_numpy()

    # use log transformation
    y_test = np.log(y_test)

    # import the models for regression
    lin = read_model(False)

    st_scaler = StandardScaler()
    st_scaler.fit(X_test)

    X_test_scaled = st_scaler.transform(X_test)

    # prediction of test set by trained model
    model_pre_test = lin.predict(X_test_scaled)
    #print(model_pre_test.isna().any())
    #model_pre_test.fillna(value=0,inplace=True)
    print("RMSE: ", np.sqrt(metrics.mean_squared_error(y_test, model_pre_test)))
    print("MAE: ", metrics.mean_absolute_error(np.exp(y_test), model_pre_test))
    print("r²: ", metrics.r2_score(y_test, model_pre_test))

    plt.scatter(model_pre_test, y_test)

    # transform data back to normal scale
    write_file("prediction_duration.csv",  np.exp(model_pre_test))


def create_classification_prediction(X, Y):

    # read saved model
    model = keras.models.load_model(os.getcwd() + r"\output_data\classif_model.h5")

    st_scaler = StandardScaler()

    st_scaler.fit(X)
    # scale predictors
    X_test_scaled = st_scaler.transform(X)

    # predict given test set
    y_pred = model.predict(X_test_scaled)

    # print metrics
    print("RMSE: ", np.sqrt(metrics.mean_squared_error(Y, y_pred)))
    print("MAE: ", metrics.mean_absolute_error(Y, y_pred))
    print("r²: ", metrics.r2_score(Y, y_pred))

    # create confusion matrix
    #print(confusion_matrix(Y, y_pred))

    #history_df = pd.DataFrame(model.history)
    #history_df

    #root_metrics_df = history_df[["mse", "val_mse"]].apply(np.sqrt)
    #root_metrics_df.rename({"mse": "rmse", "val_mse": "val_rmse"}, axis=1, inplace=True)
    #root_metrics_df

    # create loss plot for epochs
    #fig, ax = plt.subplots(1, 1, figsize=(12, 4), dpi=200)

    #ax.plot(root_metrics_df["rmse"])

    #ax.set_xlabel("Epochs")
    #ax.set_ylabel("Root Mean Squared Error")

    #ax.set_xlim([0, 20 - 1])

    #plt.show()
    write_file("prediction_classif.csv",  y_pred)
