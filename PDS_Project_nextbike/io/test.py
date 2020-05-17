import pandas as pd
import os
from .input import read_file
from .createStatisics import create_statistics
from .utils import drop_short_trips, cleaning_new_df


def testing_code(csv_file):

     df = pd.read_csv(csv_file)
     print(len(df))
     df_s = cleaning_new_df(df)
     print(len(df_s))
