import pandas as pd
import os
from .input import read_file
import folium
from .createStatisics import create_statistics
from .utils import drop_short_trips, cleaning_new_df, create_zip_code_data, drop_outlier


def testing_code(df):
     # geo_data = read_file("C:/Users/manue/git/PDS/Project/PDS_Project/data/backup-zipcodes")
     drop_outlier(df)
     # create_zip_code_data(df, geo_data)
     # df_s = cleaning_new_df(df)
