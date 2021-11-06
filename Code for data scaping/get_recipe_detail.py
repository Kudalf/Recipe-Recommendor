# -*- coding: utf-8 -*-
"""
Created on Sun Sep 26 16:07:50 2021

@author: Yifan Zhou
@github: github.com/Kudalf
@email: yifanz6@andrew.cmu.edu   
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import json
import locale

# open browser

options = Options()
options.add_argument("--headless")  
browser = webdriver.Chrome(options=options)
wait = WebDriverWait(browser, 20)


# get the recipies' urls from txt
recipe_url_list = []
with open('../Data/recipe_url.txt', 'r') as f:
    for i in f:
        recipe_url_list.append(i)

# The defalt serve number on the recipe webpage is not 1, so we set it to i = 1
def set_serve(i=1):
    button = browser.find_element_by_css_selector('#serves_txt a')
    global serve_set
    serve_set = True
    try:
        button.click()
    except Exception:
        print('cannot click. Continue')
        serve_set = False
        return
    time.sleep(0.1)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input:nth-child(1)')))
    inbox_serve = browser.find_element_by_css_selector('input:nth-child(1)')
    inbox_serve.send_keys(i)
    time.sleep(0.1)
    inbox_serve.send_keys(Keys.ENTER)
    time.sleep(0.1)
    try: 
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#serves_txt')))
    except TimeoutException as ex:
        print("Exception has been thrown. " + str(ex))
        serve_set = False
        return

# get the nutrition, ingredient and directions of every recipe
def get_nutri_ingre_direct(x):
    browser.get(x)
    global get_nutri
    get_nutri = True
    try: 
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'td')))
    except TimeoutException as ex:
        print("Exception has been thrown. " + str(ex))
        get_nutri = False
        return
   
    
    browser.maximize_window() 
    
    # set_serve to 1
    set_serve(1)
    
    if serve_set == False:
        return    
    pq_doc = pq(browser.page_source) 
    
    # get recipe name
    global recipe_name
    recipe_name = pq_doc('.recipe-view__heading').text()
    
    # get category and subcat
    global category
    category_items = pq_doc('.recipe-view__breadcrumbs a')
    category_items_list = category_items.items()
    global cat
    global subcat
    counter = 0
    for item in category_items_list:
        if counter == 0:
            counter += 1
            continue
        if counter == 1:
            counter += 1
            cat = item.text()
            continue
        if counter == 2:
            counter += 1
            subcat = item.text()
             
    # get nutrient info
    nutri_items = pq_doc('.nutrient_details')
    nutri_items_list = nutri_items.items()
    global nutri_list
    nutri_list = []
    for item in nutri_items_list:
        nutri_list.append(item.text())
    nutri_list = nutri_list[0:11]
    
    # get ingredient info
    ingre_items = pq_doc('#ingredients_list_makeover li')
    ingre_items_list = ingre_items.items()
    global ingre_list
    ingre_list = []
    for item in ingre_items_list:
        ingre_list.append(item.text())
    
    # get cooking directions
    global directions
    directions = pq_doc('#directions_standard p').text()    

cook_detail_dict = {}



# create dataframe
columnnames = ['Recipe', 'Cat', 'Subcat', 'Calories', 'Kilojoules', 'Fat', 
               'Saturated Fat', 'Cholesterol', 'Sodium', 'Carbohydrates', 
               'Fiber', 'Total Sugars', 'Protein', 'Calcium', 'URL']

recipeDF = pd.DataFrame(columns = columnnames)

for url in recipe_url_list:
    get_nutri_ingre_direct(url)
    if '-' in nutri_list:
        continue
    if serve_set == False:
        continue
    if get_nutri == False:
        continue
    nutri_list.insert(0, subcat)
    nutri_list.insert(0, cat)
    nutri_list.insert(0, recipe_name)
    nutri_list.append(url)
    recipeDF.loc[len(recipeDF)] = nutri_list
    cook_detail_dict[recipe_name] = {'ingredients': ingre_list, 'directions': directions}

with open("../Data/cooking_detail_dict.json","w") as f:
     json.dump(cook_detail_dict,f)
     print("Cooking details written into json")

# write to csv and json
recipeDF.drop_duplicates(['Recipe'], inplace = True)

recipeDF.to_csv('../Data/recipe_nutrient.csv')

browser.close()





# read from csv and json
load_df = pd.read_csv('../Data/recipe_nutrient.csv', index_col = False)
with open("../Data/cooking_detail_dict.json",'r') as load_f:
     load_dict = json.load(load_f)
     print(load_dict)

# gwt rid of unit and transfer str to float; considering there is ',' in the numbers
# import locale mudule to transfer
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
load_df['Calories'] = load_df['Calories'].apply(lambda x: locale.atof(x[:-5]))
load_df['Kilojoules'] = load_df['Kilojoules'].apply(lambda x: locale.atof(x[:-3]))
load_df['Fat'] = load_df['Fat'].apply(lambda x: locale.atof(x[:-2]))
load_df['Saturated Fat'] = load_df['Saturated Fat'].apply(lambda x: locale.atof(x[:-2]))
load_df['Cholesterol'] = load_df['Cholesterol'].apply(lambda x: locale.atof(x[:-3]))
load_df['Sodium'] = load_df['Sodium'].apply(lambda x: locale.atof(x[:-2]))
load_df['Carbohydrates'] = load_df['Carbohydrates'].apply(lambda x: locale.atof(x[:-2]))
load_df['Fiber'] = load_df['Fiber'].apply(lambda x: locale.atof(x[:-2]))
load_df['Total Sugars'] = load_df['Total Sugars'].apply(lambda x: locale.atof(x[:-2]))
load_df['Protein'] = load_df['Protein'].apply(lambda x: locale.atof(x[:-2]))
load_df['Calcium'] = load_df['Calcium'].apply(lambda x: locale.atof(x[:-3]))

load_df.to_csv('../Data/recipe_nutrient.csv', index_col = False)

