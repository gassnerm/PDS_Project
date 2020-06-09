import tensorflow

from .utils import get_data_path
import os
import pickle
import pandas as pd


def write_file(target_path,  df):
    # os.system("pip install --user tensorflow==2.00 ")
    # safe df to file

    print("Csv will be save to ","\\output_data\\" , target_path)
    file = pd.DataFrame(df)
    file.to_csv(os.path.join(os.getcwd()) + "\\output_data\\" + target_path)


def save_model(model, classif_flag):

    # save classification model
    if classif_flag:
        model.save(os.getcwd() + r"\output_data\classif_model.h5")
    # else save as regression model
    else:

        pickle.dump(model, open(os.path.join(get_data_path(), "..\\output_data\\regression_model.pkl"), 'wb'))

def save_scaler(model, classif_flag):
