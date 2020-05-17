from .utils import get_data_path
import pandas as pd
import os
import pickle


def read_file(filename):
    try:

        df = pd.read_csv(filename, dtype=str, index_col=0)

        return df

    except FileNotFoundError:

        print("Data file not found. Path was " + filename)


def read_model():
    path = os.path.join(get_data_path(), "output/model.pkl")
    with open(path, "rb") as f:
        model = pickle.load(f)
    return model
