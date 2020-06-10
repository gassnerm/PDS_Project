from .utils import get_data_path
import pandas as pd
import os
import pickle


# read file relative to data folder
def read_file(filename):
    try:

        # read file
        path = os.path.join(get_data_path(), filename)

        # read file create df out of it
        df = pd.read_csv(path, dtype=str, index_col=0)
        return df
    except (FileNotFoundError, TypeError) as e:

        # file not found catch
        print("Data file not found. Path was process terminated.")
        exit(1)


# read model for prediction
def read_model(classif):

    # load model for classification
    if classif:
        # read model from storage
        path = os.path.join(os.getcwd() + r"\output_data\classif_model.h5")
    else:
        # if regression model required
        path = os.path.join(os.getcwd() + r"\output_data\regression_model.pkl")

    # load model over pickle
    model = pickle.load(open(path, 'rb'))
    return model


# read scale for prediction
def read_scaler(classif):

    # import scaler for model to predict
    if classif:
        # read model from storage
        path = os.path.join(os.getcwd() + r"\output_data\scaler_class.pkl")
    else:
        # if regression model required
        path = os.path.join(os.getcwd() + r"\output_data\scaler_regression.pkl")

    # load model
    model = pickle.load(open(path, 'rb'))

    return model
