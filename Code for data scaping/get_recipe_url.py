# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 23:31:28 2021

@author: Yifan Zhou
@github: github.com/Kudalf
@email: yifanz6@andrew.cmu.edu   
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq

# Download your ChromeDriver from http://chromedriver.storage.googleapis.com/index.html 
# Copy your ChromeDriver.exe to \Anaconda3\Scripts 

# open chrome browser
options = Options()
options.add_argument("--headless")  # not show the browser so it will save some time
browser = webdriver.Chrome(options=options)
wait = WebDriverWait(browser, 20) # not have to wait for too long


# get categories' url
cat_url_list = []
def get_cat():
    browser.get('https://www.calorieking.com/recipes/')
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.readable a'))) # wait till the desired part is loaded
    browser.maximize_window() 
    pq_doc = pq(browser.page_source) # get the html of the website
    cat_items = pq_doc('.readable a') # use css selector to get the desired part
    cat_items_list = cat_items.items()
    for item in cat_items_list:
        cat_url_list.append('https://www.calorieking.com' + str(item.attr.href))

get_cat()    
 
# get subcategories' url    
subcat_url_list = []
def get_subcat(x):
    browser.get(x)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#recSubCat a')))
    browser.maximize_window()
    pq_doc = pq(browser.page_source) 
    subcat_items = pq_doc('#recSubCat a')
    subcat_items_list = subcat_items.items()
    for item in subcat_items_list:
        subcat_url_list.append('https://www.calorieking.com' + str(item.attr.href))

for i in cat_url_list:
    get_subcat(i)

# get the url for every recipe
recipe_url_list = []
def get_recipe_url(x):
    browser.get(x)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.readable a')))
    browser.maximize_window()
    pq_doc = pq(browser.page_source) 
    recipe_items = pq_doc('.readable a')
    recipe_items_list = recipe_items.items()
    for item in recipe_items_list:
        recipe_url_list.append('https://www.calorieking.com' + str(item.attr.href))

for i in subcat_url_list:
    get_recipe_url(i)

# save the recipe url list to txt file    
with open('../Data/recipe_url.txt', 'w') as f:
    for value in recipe_url_list: 
        f.write(value + '\n') 

browser.close()