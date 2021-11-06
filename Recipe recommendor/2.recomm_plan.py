import pandas as pd
import numpy as np
from weather import exercise

rdata = pd.read_csv('recipe_nutrient.csv')

# Get the DataFrame only for 'Breakfasts'.
rdata_bf = rdata.loc[rdata['Cat'] == 'Breakfasts']
rdata_bf = rdata_bf.reset_index(drop=True)
# Get the DataFrame only for 'Warm food'.
rdata_hot = rdata.loc[rdata['Subcat'] == 'Warm Soup, Stew and Chili']
rdata_hot = rdata_hot.reset_index(drop=True)

# Get the DataFrame only for meals other than desserts or tapas etc.
cat_list = list(rdata['Cat'])
cat_set = set(cat_list)
not_meal = ['Appetizers, Dips and Snacks', 'Baking',
            'Beverages', 'Breakfasts', 'Desserts',
            'Sauces, Dressings, Condiments, Creams']
for i in not_meal:
    cat_set.remove(i)
cat_list = list(cat_set)
cat_list.sort()

rdata_meal = rdata[rdata['Cat'].isin(cat_list)]
rdata_meal = rdata_meal.reset_index(drop=True)

# Assign the data for exercises and the daily temperature to e_data and tem.
e_data, tem, date = exercise()




def recomm(i): # i is the daily calorie intake. These two are calculated from user input.
    if i > 3000:
        return 'Too much to eat'
    while True:
        # Reset the count, eat_calo and recipe_list.
        count = 0
        eat_calo = i 
        recipe_list = []
        bf_rad = np.random.randint(0, len(rdata_bf) - 1)
        hot_rad = np.random.randint(0, len(rdata_hot) - 1)
        # Recommend a breakfast. If the recommended breakfast takes up too much of the daily calorie intake, 
        # the options would break the function and print "high calorie breakfast". In this case, please rerun the program for a new set of recommendations.
        if eat_calo - rdata_bf['Calories'].iloc[bf_rad] > 0:
            recipe_list.append(rdata_bf['Recipe'].iloc[bf_rad])
            eat_calo -= rdata_bf['Calories'].iloc[bf_rad]
        else:
            print('High calorie breakfast')
            break
        # If cold weather, recommend to eat a kind of hot food.
        if tem < 12:
        # The program recommends a soup if daily intake limit allows for additional intake. If the recommended soup takes up too much of the daily calorie allocation, 
        # the options would break the function and print "high calorie breakfast and soup". In this case, please rerun the program for a new set of recommendations.
            if eat_calo - rdata_hot['Calories'].iloc[hot_rad] > 0:
                recipe_list.append(rdata_hot['Recipe'].iloc[hot_rad])
                eat_calo -= rdata_hot['Calories'].iloc[hot_rad]
            else:
                print('High calorie breakfast and soup')
                break
        # Select random dishes from rdata_meal, while intake limit allows, append them to a list.
        meal_rad = np.random.randint(0, len(rdata_meal) - 1)
        while eat_calo - rdata_meal['Calories'].iloc[meal_rad] >= 0:
            eat_calo -= rdata_meal['Calories'].iloc[meal_rad]
            recipe_list.append(rdata_meal['Recipe'].iloc[meal_rad])
            count += 1
            meal_rad = np.random.randint(0, len(rdata_meal) - 1)
        if count < ((i // 228) - 2): # Control the number of dishes to save cooking time.
            break
    return recipe_list # A list with daily randomly selected dishes including breakfast (maybe hot soup), is returned.

def recomm_e(o, w):  # o is the daily calorie burnt by exercise calculated from user input; w is the weight that user input.
    e_data['CalorieBurnt'] = e_data['Calories / lb'] * w
    # Create the list.
    exercise_list = []
    # Select random exercise(s) from e_data, append them to a list until the daily calorie burnt by exercise is fullfilled.
    while o >= 0:
        exercise_rad = np.random.randint(0, len(e_data) - 1)
        o -= e_data['CalorieBurnt'].iloc[exercise_rad]
        exercise_list.append(e_data['Activity, Exercise or Sport (1 hour)'].iloc[exercise_rad])
    return exercise_list  # Return a list of randomly selected exercises.


