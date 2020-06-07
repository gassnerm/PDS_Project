
from .utils import get_data_path
import pandas as pd
import os
import pickle


def read_file(filename):
    try:

        # read file
        path = os.path.join(get_data_path(), filename)

        # read file create df out of it
        df = pd.read_csv(path, dtype=str, index_col=0)

        return df

    except FileNotFoundError:

        # file not found catch
        print("Data file not found. Path was " + filename)


# read model for prediction
def read_model(classif):

    if classif:
        # read model from storage
        path = os.path.join(os.getcwd() + r"\output_data\classif_model.h5")
    else:
        # if regression model required
        path = os.path.join(os.getcwd() + r"\output_data\regression_model.pkl")

    model = pickle.load(open(path, 'rb'))
    return model


