import numpy as np
import pandas as pd
import re
import os
import urllib.request

from url_fetcher import fetch_coordinates

adventure_idx = 0
adventure_dict = {}

for sample_html_filename in os.listdir('./Adventure_Recommendation/HTMLs/'):
    
    print(sample_html_filename)
    sample_html = './Adventure_Recommendation/HTMLs/' + sample_html_filename
    html_file = open(sample_html, 'r').read()

    search_str = re.findall("RESULT CARD BEGIN.*RESULT CARD END", html_file, re.DOTALL)[0]
    search_results = re.finditer("result-card-content", search_str)

    search_results_idx = [m.start(0) for m in search_results]
    search_results_content = []
    for idx in range(len(search_results_idx) - 1):
        search_results_content.append(search_str[search_results_idx[idx]: search_results_idx[idx + 1]])
    search_results_content.append(search_str[search_results_idx[-1]:])

    titles = [re.findall("result-content-heading.*</a>", x)[0].split('>')[-2].split('<')[0].strip() for x in search_results_content]
    for title in titles:
        if(len(title.strip()) == 0):
            print("ERROR!")
    
    link_titles = ['https://www.thrillophilia.com' + re.findall("result-card-content-section.*\n.*class", x)[0][:-6].split('=')[-1].replace('"', '') for x in search_results_content]

    lats = []
    lons = []
    
    for link_title in link_titles:
        print(link_title)
        fp = urllib.request.urlopen(link_title)
        html_content = fp.read()

        html_content = html_content.decode("utf8")
        fp.close()

        x = set(re.findall("https://maps\.google\.com/[^\&\"\']+ftid[^\&\"\']+:[^\&\"\']+", html_content))
        if(len(x) != 1):
            lat = np.nan
            lon = np.nan
        else:
            refreshed_url = [*x][0].replace("\\u0026", '&')
            lon, lat = fetch_coordinates(refreshed_url)
        lons.append(lon)
        lats.append(lat)

    rating = [re.findall("numeric-rating.*star-rating", x, re.DOTALL)[0] for x in search_results_content]
    rating = [float(re.findall("\d\.\d", x)[0]) for x in rating]

    price = [re.findall("current-price [^/]*</", x, re.DOTALL)[0] for x in search_results_content]
    price = [float(re.findall("INR [\d,\n ]*<", x, re.DOTALL)[0][4:-1].strip().replace(',', '')) for x in price]

    locations = []
    for x in search_results_content:
        try:
            location = re.findall("icon-pin.*\n.*</p>", x)[0][:-4].split('>')[-1].strip()
        except:
            location = ''
        locations.append(location)

    durations = []
    for x in search_results_content:
        try:
            duration = re.findall("icon-watch.*\n.*\n.*\n.*</p>", x)[0][:-4].split('>')[-1].strip()
        except:
            duration = ''
        durations.append(duration)

    # print(len(price))
    assert(len(titles) == len(rating))
    assert(len(rating) == len(price))
    assert(len(price) == len(locations))
    assert(len(locations) == len(durations))
    assert(len(durations) == len(lats))
    assert(len(lats) == len(lons))

    def clean_str(string):
        return string.replace("&amp;", "&").replace(",", "").replace(";", "")

    for idx in np.arange(len(titles)):
        adventure_dict_content = {}
        adventure_dict_content['title'] = clean_str(titles[idx])
        adventure_dict_content['price'] = price[idx]
        adventure_dict_content['rating'] = rating[idx]
        adventure_dict_content['location'] = locations[idx]
        adventure_dict_content['duration'] = durations[idx]
        adventure_dict_content['category'] = sample_html_filename.split('.')[0]
        adventure_dict_content['lat'] = lats[idx]
        adventure_dict_content['lon'] = lons[idx]
        adventure_dict[adventure_idx] = adventure_dict_content
        adventure_idx += 1

adventure_df = pd.DataFrame.from_dict(adventure_dict, orient = 'index')
adventure_df.to_csv('./Adventure_Recommendation/Data/adventures.csv', index = False)
print(adventure_df.head())