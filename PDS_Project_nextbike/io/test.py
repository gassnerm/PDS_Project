import pandas as pd
import os
from .input import read_file
import folium
from .createStatisics import create_statistics
from .utils import cleaning_new_df, create_zip_code_data


def testing_code(df):
    print("Hallo")
     # geo_data = read_file("C:/Users/manue/git/PDS/Project/PDS_Project/data/backup-zipcodes")
     #drop_outlier(df)
     # create_zip_code_data(df, geo_data)
     # df_s = cleaning_new_df(df)
