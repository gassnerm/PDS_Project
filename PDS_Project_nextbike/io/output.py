from .utils import get_data_path
import os
import pickle
import pandas as pd


def write_file(target_path,  df):
    # safe df to file
    print("Csv will be save to ", os.path.join(os.getcwd(), target_path))
    file = pd.DataFrame(df)
    file.to_csv(os.path.join(os.getcwd()) + "\\output_data\\" + target_path)


def save_model(model):
    pickle.dump(model, open(os.path.join(get_data_path(), "output/model.pkl"), 'wb'))