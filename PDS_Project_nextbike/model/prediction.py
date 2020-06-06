from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn import metrics
import pandas as pd
from ..io import read_model, plt, write_file
import numpy as np
from tensorflow import keras
import os


def create_duration_prediction(X_test, y_test, d):

    # set to array
    X_test = X_test.to_numpy()
    y_test = y_test.to_numpy()

    # use log transformation
    y_test = np.log(y_test)

    # determine the degree of the regression
    poly_reg = PolynomialFeatures(degree=d)

    # Create polynomial features for the 15 predictors fit transform no scaler needed
    x_poly_matrix = poly_reg.fit_transform(X_test.reshape(-1, 23))

    # regression required so false
    lin = read_model(False)

    # get the coefficients of regression.
    beta = pd.Series(index=list(poly_reg.get_feature_names()), data=lin.coef_.reshape(-1, 2600)[0])

    # set required regression coeffi.
    regressionCoef = pd.Series(beta,
                               index=['x0', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10', 'x11', 'x0^2',
                                      'x1^2', 'x2^2', 'x3^2', 'x4^2', 'x5^2', 'x6^2', 'x7^2', 'x8^2', 'x9^2', 'x10^2',
                                      'x11^2'])

    # prediction of test set by trained model
    model_pre_test = lin.predict(poly_reg.fit_transform(X_test))

    print("RMSE: ", np.sqrt(metrics.mean_squared_error(model_pre_test, y_test)))
    print("MAE: ", metrics.mean_absolute_error(model_pre_test, y_test))
    print("r²: ", metrics.r2_score(model_pre_test, y_test))

    plt.scatter(y_test, y_test)

    # transform data back to normal scale
    write_file("prediction_duration.csv",  np.exp(y_test))


def create_classification_prediction(X, Y):

    # read saved model
    model = keras.models.load_model(os.getcwd() + r"\output_data\classif_model.h5")

    model = read_model(True)
    st_scaler = StandardScaler()

    # scale predictors
    X_test_scaled = st_scaler.transform(X)

    # predict given test set
    y_pred = model.predict(X_test_scaled)

    # print metrics
    print("RMSE: ", np.sqrt(metrics.mean_squared_error(Y, y_pred)))
    print("MAE: ", metrics.mean_absolute_error(Y, y_pred))
    print("r²: ", metrics.r2_score(Y, y_pred))

    # create confusion matrix
    print(confusion_matrix(Y, y_pred))

    history_df = pd.DataFrame(model.history)
    history_df

    root_metrics_df = history_df[["mse", "val_mse"]].apply(np.sqrt)
    root_metrics_df.rename({"mse": "rmse", "val_mse": "val_rmse"}, axis=1, inplace=True)
    root_metrics_df

    # create loss plot for epochs
    fig, ax = plt.subplots(1, 1, figsize=(12, 4), dpi=200)

    ax.plot(root_metrics_df["rmse"])

    ax.set_xlabel("Epochs")
    ax.set_ylabel("Root Mean Squared Error")

    ax.set_xlim([0, 20 - 1])

    plt.show()
    write_file("prediction_classif.csv",  y_pred)
