from recommend import recommend
import pandas as pd
import numpy as np

recommended_activities = recommend()

def handle_nans(val, comma = True):
    if(pd.isnull(val)):
        if(comma == True):
            return '""'
        else:
            return ""
    return val

id = 1
rec_strs = []
for idx, activities in enumerate(recommended_activities):
    activity_strs = []
    for activity_idx in range(activities.shape[0]):
        activity_str = """
        {{
            id: {},
            name: "{}",
            price: {},
            location: "{}",
            duration: {},
            rating: {},
            distance: {}
        }}
        """
        activity_str = activity_str.format(
            id,
            handle_nans(activities.iloc[activity_idx]['title'], False),
            handle_nans(activities.iloc[activity_idx]['price']),
            handle_nans(activities.iloc[activity_idx]['location'], False),
            handle_nans(activities.iloc[activity_idx]['duration_hours']),
            handle_nans(activities.iloc[activity_idx]['rating']),
            handle_nans(np.round(activities.iloc[activity_idx]['distance'], 1)))
        id += 1
        activity_strs.append(activity_str)
    activity_strs = "activities: [" + ','.join(activity_strs) + "]"
    rec_str = """
    var recommendations{} = {{
        category: "{}",
        {}
    }};
    """
    rec_str = rec_str.format(idx + 1, activities.iloc[0]['category'].title(), activity_strs)
    rec_strs.append(rec_str)
    
rec_strs = '\n'.join(rec_strs) + "\n\nexport { recommendations1, recommendations2, recommendations3 };"

data_js = open("./WebDev/JSON/recommendation_data.js", 'w')
data_js.write(rec_strs)