from .utils import get_data_path
import os
import pickle
import pandas as pd


def write_file(target_path,  df):

    # safe df to file
    print("Csv will be save to ", "\\output_data\\" , target_path)
    file = pd.DataFrame(df)

    file.to_csv(os.path.join(os.getcwd()) + "\\output_data\\" + target_path)


# save the model to output_data folder
def save_model(model, classif_flag):

    # save classification model
    if classif_flag:
        # save model over tensaflow build in option
        model.save(os.getcwd() + r"\output_data\classif_model.h5")

    # else save as regression model
    else:
        # save model with pickel
        pickle.dump(model, open(os.path.join(get_data_path(), "..\\output_data\\regression_model.pkl"), 'wb'))


# save scale to file output folder
def save_scaler(scaler, classif_flag):

    if classif_flag:

        print("Scaler safe to scaler_class.pkl")
        pickle.dump(scaler, open(os.path.join(get_data_path(), "..\\output_data\\scaler_class.pkl"), 'wb'))
    else:

        print("Scaler safe to scaler_regression.pkl")
        pickle.dump(scaler, open(os.path.join(get_data_path(), "..\\output_data\\scaler_regression.pkl"), 'wb'))