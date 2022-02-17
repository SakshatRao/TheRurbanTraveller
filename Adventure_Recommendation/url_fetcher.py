import numpy as np
from selenium import webdriver
from url2coordinates import url2coordinates

# link = "https://maps.google.com/?q=Kolad,+Maharashtra+402304,+India&ftid=0x3be83d9500b571b1:0x52cac93070d849d3"

def fetch_coordinates(link):
    driver = webdriver.Firefox(executable_path='/home/sakshat/Downloads/geckodriver')
    driver.get(link)
    while('!3d' not in driver.current_url):
        pass
    refreshed_url = driver.current_url
    driver.close()

    return url2coordinates(refreshed_url)