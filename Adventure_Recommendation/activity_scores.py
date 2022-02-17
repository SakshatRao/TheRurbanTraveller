import numpy as np
import pandas as pd
import re
from geopy import distance, Point

from current_location import curr_loc
activity_data = pd.read_csv("./Adventure_Recommendation/Data/adventures.csv")

def find_approx_dist(loc1, loc2):
    if(np.isnan(loc1[0]) or np.isnan(loc1[1])):
        return np.nan
    else:
        p1 = Point(latitude = loc1[0], longitude = loc1[1])
        p2 = Point(latitude = loc2[0], longitude = loc2[1])
        return distance.geodesic(p1, p2).km

activity_data['distance'] = activity_data.apply(lambda x: find_approx_dist((x['lat'], x['lon']), curr_loc), axis = 1)

def determine_duration(dur):
    if(pd.isnull(dur)):
        return np.nan
    hour_check = re.search("\d+H", dur)
    if(hour_check):
        return float(hour_check.group(0)[:-1])
    day_check = re.search("\d+[DN]", dur)
    if(day_check):
        return float(day_check.group(0)[:-1]) * 24
    return -1

activity_data['duration_hours'] = activity_data['duration'].apply(determine_duration)

activity_embeddings = activity_data[['distance', 'rating', 'price', 'duration_hours']].values
activity_embeddings = (activity_embeddings - np.nanmean(activity_embeddings, axis = 0)) / np.nanstd(activity_embeddings, axis = 0)
activity_embeddings = np.nan_to_num(activity_embeddings)
activity_embeddings = (-activity_embeddings[:, 0] * 5) + (activity_embeddings[:, 1] * 4) + (-activity_embeddings[:, 2] * 3) + (-activity_embeddings[:, 3] * 1)
activity_data = activity_data.assign(pref_score = activity_embeddings)

activity_data.to_csv("./Adventure_Recommendation/Data/adventures_processed.csv", index = False)