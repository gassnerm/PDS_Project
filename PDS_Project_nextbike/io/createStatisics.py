

def create_statistics(df):

    Stat_Fe = df[list(map(lambda x: str(df.loc[x]["Starttime"])[5:7] == "02", df.index()))]["duration"].describe()
    Stat_Ma = df[list(map(lambda x: str(df.loc[x]["Starttime"])[5:7] == "03", df.index()))]["duration"].describe()
    Stat_Ap = df[list(map(lambda x: str(df.loc[x]["Starttime"])[5:7] == "04", df.index()))]["duration"].describe()
    Stat_May = df[list(map(lambda x: str(df.loc[x]["Starttime"])[5:7] == "05", df.index()))]["duration"].describe()
    Stat_Ju = df[list(map(lambda x: str(df.loc[x]["Starttime"])[5:7] == "06", df.index()))]["duration"].describe()
    Stat_Jul = df[list(map(lambda x: str(df.loc[x]["Starttime"])[5:7] == "07", df.index()))]["duration"].describe()
    Stat_Au = df[list(map(lambda x: str(df.loc[x]["Starttime"])[5:7] == "08", df.index()))]["duration"].describe()
    Stat_Se = df[list(map(lambda x: str(df.loc[x]["Starttime"])[5:7] == "09", df.index()))]["duration"].describe()
    Stat_Oc = df[list(map(lambda x: str(df.loc[x]["Starttime"])[5:7] == "10", df.index()))]["duration"].describe()
    Stat_No = df[list(map(lambda x: str(df.loc[x]["Starttime"])[5:7] == "11", df.index()))]["duration"].describe()
    Stat_De = df[list(map(lambda x: str(df.loc[x]["Starttime"])[5:7] == "12", df.index()))]["duration"].describe()

    print(Stat_Ju)
