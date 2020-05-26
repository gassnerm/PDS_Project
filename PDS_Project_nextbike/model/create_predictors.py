import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

df = pd.read_csv(r"/output_data/transform_DF", index_col=0)

df_mapping = pd.Series({0: "Monday",
                        1: "Tuesday",
                        2: "Wednesday",
                        3: "Thurday",
                        4: "Friday",
                        5: "Saturday",
                        6: "Sunday"})


holiday_winter = dt.datetime(2019, 1, 12)
holiday_spring = dt.datetime(2019, 4, 27)
holiday_sommer = dt.datetime(2019, 8, 9)
holiday_fall = dt.datetime(2019, 10, 12)
holiday_crism = dt.datetime(2019, 12, 31)


date_list = pd.Series([str(holiday_winter - dt.timedelta(days=x)) for x in range(0,12)], dtype=str)
date_list2 = pd.Series([str(holiday_spring - dt.timedelta(days=x)) for x in range(0,12)], dtype=str)
date_list3 = pd.Series([str(holiday_sommer - dt.timedelta(days=x)) for x in range(0,40)], dtype=str)
date_list4 = pd.Series([str(holiday_fall - dt.timedelta(days=x)) for x in range(0,13)], dtype=str)
date_list5 = pd.Series([str(holiday_crism - dt.timedelta(days=x)) for x in range(0,9)], dtype=str)

date_list = date_list.append(date_list2, ignore_index=False).reset_index(drop = True)
date_list = date_list.append(date_list3, ignore_index=False).reset_index(drop = True)
date_list = date_list.append(date_list4, ignore_index=False).reset_index(drop = True)
date_list = date_list.append(date_list5, ignore_index=False).reset_index(drop = True)


df_holiday = pd.Series({0: "2019-05-01",
                        1: "2019-05-30",
                        2: "2019-06-10",
                        3: "2019-06-20"})

df_holiday = df_holiday.append(date_list.astype(str)).reset_index(drop=True)
df_holiday = pd.Series(index=df_holiday.index, data=list(map(lambda x: str(x[0:10]), df_holiday.values)))


df["day"] = pd.Series(index=df.index,data=list(map(lambda x: df_mapping[int(pd.to_datetime(str(x)).weekday())], df["Starttime"])))

df["hour"] = pd.Series(index=df.index, data=list(map(lambda x: str(df.loc[x]["Starttime"])[11:13], df.index)))

df["holiday"] = pd.Series(index=df.index, data=list(map(lambda x: df.loc[x]["Starttime"][0:10] in df_holiday.values, df.index)))


# Separate the df by month of day
Stat_Ja = df[list(map(lambda x: str(df.loc[x]["Starttime"])[5:7] == "01", df.index))]
Stat_Fe = df[list(map(lambda x: str(df.loc[x]["Starttime"])[5:7] == "02", df.index))]
Stat_Ma = df[list(map(lambda x: str(df.loc[x]["Starttime"])[5:7] == "03", df.index))]
Stat_Ap = df[list(map(lambda x: str(df.loc[x]["Starttime"])[5:7] == "04", df.index))]
Stat_May = df[list(map(lambda x: str(df.loc[x]["Starttime"])[5:7] == "05", df.index))]
Stat_Ju = df[list(map(lambda x: str(df.loc[x]["Starttime"])[5:7] == "06", df.index))]
Stat_Jul = df[list(map(lambda x: str(df.loc[x]["Starttime"])[5:7] == "07", df.index))]
Stat_Au = df[list(map(lambda x: str(df.loc[x]["Starttime"])[5:7] == "08", df.index))]
Stat_Se = df[list(map(lambda x: str(df.loc[x]["Starttime"])[5:7] == "09", df.index))]
Stat_Oc = df[list(map(lambda x: str(df.loc[x]["Starttime"])[5:7] == "10", df.index))]
Stat_No = df[list(map(lambda x: str(df.loc[x]["Starttime"])[5:7] == "11", df.index))]
Stat_De = df[list(map(lambda x: str(df.loc[x]["Starttime"])[5:7] == "12", df.index))]


# Separate the df by weekdays
Stat_Mo = df[list(map(lambda x: pd.to_datetime(df.loc[x]["Starttime"]).weekday() == 0, df.index))]
Stat_Tu = df[list(map(lambda x: pd.to_datetime(df.loc[x]["Starttime"]).weekday() == 1, df.index))]
Stat_We = df[list(map(lambda x: pd.to_datetime(df.loc[x]["Starttime"]).weekday() == 2, df.index))]
Stat_Th = df[list(map(lambda x: pd.to_datetime(df.loc[x]["Starttime"]).weekday() == 3, df.index))]
Stat_Fr = df[list(map(lambda x: pd.to_datetime(df.loc[x]["Starttime"]).weekday() == 4, df.index))]
Stat_Sa = df[list(map(lambda x: pd.to_datetime(df.loc[x]["Starttime"]).weekday() == 5, df.index))]
Stat_Su = df[list(map(lambda x: pd.to_datetime(df.loc[x]["Starttime"]).weekday() == 6, df.index))]


# Separate the df by hour of day
Start_Time_0 = df[list(map(lambda x: str(df.loc[x]["Starttime"])[11:13] == "00", df.index))]
Start_Time_01 = df[list(map(lambda x: str(df.loc[x]["Starttime"])[11:13] == "01", df.index))]
Start_Time_02 = df[list(map(lambda x: str(df.loc[x]["Starttime"])[11:13] == "02", df.index))]
Start_Time_03 = df[list(map(lambda x: str(df.loc[x]["Starttime"])[11:13] == "03", df.index))]
Start_Time_04 = df[list(map(lambda x: str(df.loc[x]["Starttime"])[11:13] == "04", df.index))]
Start_Time_05 = df[list(map(lambda x: str(df.loc[x]["Starttime"])[11:13] == "05", df.index))]
Start_Time_06 = df[list(map(lambda x: str(df.loc[x]["Starttime"])[11:13] == "06", df.index))]
Start_Time_07 = df[list(map(lambda x: str(df.loc[x]["Starttime"])[11:13] == "07", df.index))]
Start_Time_08 = df[list(map(lambda x: str(df.loc[x]["Starttime"])[11:13] == "08", df.index))]
Start_Time_09 = df[list(map(lambda x: str(df.loc[x]["Starttime"])[11:13] == "09", df.index))]
Start_Time_10 = df[list(map(lambda x: str(df.loc[x]["Starttime"])[11:13] == "10", df.index))]
Start_Time_11 = df[list(map(lambda x: str(df.loc[x]["Starttime"])[11:13] == "11", df.index))]

Start_Time_12 = df[list(map(lambda x: str(df.loc[x]["Starttime"])[11:13] == "12", df.index))]
Start_Time_13 = df[list(map(lambda x: str(df.loc[x]["Starttime"])[11:13] == "13", df.index))]
Start_Time_14 = df[list(map(lambda x: str(df.loc[x]["Starttime"])[11:13] == "14", df.index))]
Start_Time_15 = df[list(map(lambda x: str(df.loc[x]["Starttime"])[11:13] == "15", df.index))]
Start_Time_16 = df[list(map(lambda x: str(df.loc[x]["Starttime"])[11:13] == "16", df.index))]
Start_Time_17 = df[list(map(lambda x: str(df.loc[x]["Starttime"])[11:13] == "17", df.index))]
Start_Time_18 = df[list(map(lambda x: str(df.loc[x]["Starttime"])[11:13] == "18", df.index))]
Start_Time_19 = df[list(map(lambda x: str(df.loc[x]["Starttime"])[11:13] == "19", df.index))]
Start_Time_20 = df[list(map(lambda x: str(df.loc[x]["Starttime"])[11:13] == "20", df.index))]
Start_Time_21 = df[list(map(lambda x: str(df.loc[x]["Starttime"])[11:13] == "21", df.index))]
Start_Time_22 = df[list(map(lambda x: str(df.loc[x]["Starttime"])[11:13] == "22", df.index))]
Start_Time_23 = df[list(map(lambda x: str(df.loc[x]["Starttime"])[11:13] == "23", df.index))]

## Month duration mean()

month_duration = pd.Series({"Januar" : Stat_Ja["duration"].mean(),
                            "Februar" : Stat_Fe["duration"].mean(),
                            "March" : Stat_Ma["duration"].mean(),
                            "April" : Stat_Ap["duration"].mean(),
                            "Mai" : Stat_May["duration"].mean(),
                            "June" : Stat_Ju["duration"].mean(),
                            "July" : 0,
                            "August": Stat_Au["duration"].mean(),
                            "September": Stat_Se["duration"].mean(),
                            "October": Stat_Oc["duration"].mean(),
                            "November": Stat_No["duration"].mean(),
                            "December": Stat_De["duration"].mean()})
month_duration

month_duration_mean = [month_duration.values.mean(),month_duration.values.mean(), month_duration.values.mean(),
                       month_duration.values.mean(), month_duration.values.mean(), month_duration.values.mean(),
                       month_duration.values.mean(), month_duration.values.mean(), month_duration.values.mean(),
                       month_duration.values.mean(), month_duration.values.mean(), month_duration.values.mean()]

sns.barplot(month_duration.keys(), month_duration.values)
plt.plot(month_duration.keys(), month_duration_mean)
gcf = plt.gcf()
gcf.set_figwidth(15)
gcf.set_figheight(10)
plt.show()


month_number = pd.Series({"Januar": Stat_Ja["duration"].count(),
                          "Februar": Stat_Fe["duration"].count(),
                           "March": Stat_Ma["duration"].count(),
                           "April": Stat_Ap["duration"].count(),
                            "Mai": Stat_May["duration"].count(),
                            "June": Stat_Ju["duration"].count(),
                            "July": Stat_Jul["duration"].count(),
                            "August": Stat_Au["duration"].count(),
                            "September": Stat_Se["duration"].count(),
                            "October": Stat_Oc["duration"].count(),
                            "November": Stat_No["duration"].count(),
                            "December": Stat_De["duration"].count()})
month_number


ax = sns.barplot(month_number.keys(), month_number.values)
gcf = plt.gcf()
gcf.set_figwidth(15)
gcf.set_figheight(10)
plt.show()

df["holiday"]
df_holiday



def create_predictors_classifiaction():
