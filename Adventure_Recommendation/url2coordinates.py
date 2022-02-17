import re
import numpy as np

def url2coordinates(link):
    lat_lon = re.findall("\\d+\\.\\d+,\\d+\\.\\d+", link)[0]
    lat = lat_lon.split(',')[1]
    lon = lat_lon.split(',')[0]
    return float(lon), float(lat)

# sample_link = "https://www.google.com/maps/place/Kolad,+Maharashtra+402304/@18.4057277,73.2002087,15z/data=!3m1!4b1!4m5!3m4!1s0x3be83d9500b571b1:0x52cac93070d849d3!8m2!3d18.4077066!4d73.2101837"
# print(url2coordinates(sample_link))