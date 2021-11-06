# Recipe-Recommendor

## Abstract

Team Achilles collaborated to develop a program in Python that provides recommendations on daily meal and exercise plans based on users’ weight loss goals. Additionally, the program is designed to generate tailored plans that are adjusted by lifestyle preferences and projected weather conditions. Once a user feeds their basic information, weight loss goals, preferences, and ideal start date into the interface, our program is able to return recommendations that will help the user achieve their ideal weight within the desired time frame. Along with the meal plan recommendation, a shopping list containing ingredients necessary for the recipes is also provided within the program. Furthermore, data visualizations on recipe nutrition distribution and weight loss progression are included to enhance user experience. The project database was constructed with structured [weather data][1] retrieved by API, [recipe and nutritional information][2] obtained from web scraping, and [exercise information][3] retrieved in a CSV format.


## User Instructions

### Installation 
Please install the following packages if you don't have them locally installed.
selenium
tkinter
pandas
pyquery
numpy
json
requests
csv
datetime
time
locale

### Data update
To get the updated recipe data from thet website, run 'Code for data scaping\get_recipe_url.py' first, then run 'Code for data scaping\get_recipe_detail.py'. The data will be stored in the ‘/Data’ file.
### Run 'Recipe recommendor\1.main program.py' to start the main program.

### User Input 
Gender Input - Please enter either “M” for Male or “F” for Female to indicate the user’s gender
Age Input - Please enter an integer between 0 to 100. Entering a number below 18 will result in users seeing a message designed to discourage minors from using this program
Date Input - Please enter today date by MM-DD (example: 01-01)
Baseline_Food - This variable sets the baseline calorie intake at 1,800/day. If a user indicates that they prioritize a lax meal plan over a light exercise plan, this variable becomes the baseline of their daily caloric intake and a more rigorous workout plan is likely recommended in order to accomplish user’s weight loss goals
Baseline_Exercise - This variable sets the baseline calorie burn from workouts at 500/day. If a user indicates that they prioritize a light workout plan over a demanding one, this variable becomes the baseline of their daily exercise burn and a more stringent plan in terms of calorie intake is likely recommended in order to accomplish user’s weight loss goals
Plan Preference - This step allows users to enter their preference between a restrictive diet and a rigorous workout plan to better align the program to user needs.
Cooking Directions - This step prints out cooking instructions corresponding to the user’s unique meal plan if the user has indicated that they would like to see cooking instructions.

### Output
Graph - Distribution of Calories in the Recipe Pool 
Exercise Recommendation - Exercise output is provided in a per hour unit. Our program merely provides workout recommendations - users have the flexibility to replace certain exercises in their daily routine based on their interests.
Daily Recipe - The program returns meals in the order of breakfast, and other dishes, customized to the user’s calorie intake limits and the temperature of the day. If the program presumes that the temperature is below 50 degrees fahrenheit, a soup or stew is included in the daily meal recommendations. 
Shopping List - The program returns a daily shopping list for users based on daily recipe recommendation. Each kind of ingredient as well as its amount occupies 1 row, while all ingredients needed for per meal are listed together.





[1]: https://www.worldweatheronline.com/developer/
[2]: https://www.calorieking.com/
[3]: https://www.kaggle.com/aadhavvignesh/calories-burned-during-exercise-and-activities/version/2
