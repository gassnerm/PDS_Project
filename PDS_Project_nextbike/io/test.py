import pandas as pd
import os
from .input import read_file

from .createStatisics import create_statistics
from .utils import drop_short_trips, cleaning_new_df, create_zip_code_data


def testing_code(df):

     geo_data = read_file("C:/Users/manue/backup_zipcodes")
     create_zip_code_data(df, geo_data)
     print(len(df))
     df_s = cleaning_new_df(df)
     print(len(df_s))