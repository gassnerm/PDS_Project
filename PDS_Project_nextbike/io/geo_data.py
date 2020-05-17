from geopy.geocoders import Nominatim
from ratelimit import limits, sleep_and_retry
import pandas as pd
import numpy as np

index_location = df["Start_Latitude"].str.cat(df["Start_Longitude"], sep=", ").value_counts().index

gc = Nominatim(user_agent="fintu-blog-geocoding-python", timeout=10)


@sleep_and_retry
@limits(1, 1)
def rate_limited_geocode(query):
    try:
        s = gc.geocode(query)[0].split(",")[-2].lstrip()
        print(s)
        print(query)
    except TypeError as e:
        return "ERROR"
    except IndexError as e2:
        return "ERROR"
    return s


def geocode(cordinates):
    lookup_query = cordinates
    lookup_result = rate_limited_geocode(lookup_query)

    return lookup_result

# df["geo_location"] = df.progress_apply(geocode, axis=1)
x = pd.Series(index= index_location[:1000], data = list(map(lambda x: geocode(x), index_location[:1000])))
print("x")
x1 = pd.Series(index= index_location[1000:2000], data = list(map(lambda x: geocode(x), index_location[1000:2000])))
print("x1")
x2 = pd.Series(index= index_location[2000:3000], data = list(map(lambda x: geocode(x), index_location[2000:3000])))
print("x2")
x3 = pd.Series(index= index_location[3000:4000], data = list(map(lambda x: geocode(x), index_location[3000:4000])))
print("x3")
x4 = pd.Series(index= index_location[4000:5000], data = list(map(lambda x: geocode(x), index_location[4000:5000])))
print("x4")
x5 = pd.Series(index= index_location[5000:6000], data = list(map(lambda x: geocode(x), index_location[5000:6000])))
print("x5")
x6 = pd.Series(index= index_location[6000:7000], data = list(map(lambda x: geocode(x), index_location[6000:7000])))
print("x6")
x7 = pd.Series(index= index_location[7000:8000], data = list(map(lambda x: geocode(x), index_location[7000:8000])))
print("x7")
x8 = pd.Series(index= index_location[8000:9000], data = list(map(lambda x: geocode(x), index_location[8000:9000])))
print("x8")
x9 = pd.Series(index= index_location[9000:10000], data = list(map(lambda x: geocode(x), index_location[9000:10000])))
x10 = pd.Series(index= index_location[10000:11000], data = list(map(lambda x: geocode(x), index_location[10000:11000])))
print("x10")
x11 = pd.Series(index= index_location[11000:12000], data = list(map(lambda x: geocode(x), index_location[11000:12000])))
print("x11")
x12 = pd.Series(index= index_location[12000:13000], data = list(map(lambda x: geocode(x), index_location[12000:13000])))
print("x12")
x13 = pd.Series(index= index_location[13000:14000], data = list(map(lambda x: geocode(x), index_location[13000:14000])))
print("x13")

x14 = pd.Series(index= index_location[14000:15000], data = list(map(lambda x: geocode(x), index_location[14000:15000])))
print("x14")
x15 = pd.Series(index= index_location[15000:], data = list(map(lambda x: geocode(x), index_location[15000:])))


zipcodes_Array = x.append(x1).append(x2).append(x3).append(x4).append(x5).append(x6).append(x7)\
    .append(x8).append(x9).append(x10).append(x11).append(x12).append(x13).append(x14).append(x15)


zipcode_df =  pd.DataFrame(zipcodes_Array)
zipcode_df.columns = ["zipcodes"]

