 #In this version, we use the `SequenceMatcher` class from the `difflib` module to find the closest matching recipe. We first create a list of available ingredients, as before. If no compatible recipes are found, we use the `max()` function to find the key in the `RECIPES` dictionary with the highest matching ratio to the available ingredients. The matching ratio is calculated using the `SequenceMatcher` class, which compares the available ingredients to each recipe name and returns a value between 0 and 1 indicating the similarity. When the program is run and no compatible recipes are found, the user will see a message indicating the closest matching recipe based on their available ingredients.

from tkinter import *
from difflib import SequenceMatcher 

INGREDIENTS = ['flour', 'sugar', 'salt', 'eggs', 'milk', 'butter', 'cocoa powder', 'baking powder', 'vanilla extract', 'spaghetti', 'pancetta', 'parmigiano reggiano', 'pecorino romano', 'black pepper', 'onion', 'garlic', 'chicken or vegetable broth', 'olive oil', 'sugar', 'pepper', 'whole chicken', 'lemon', 'thyme', 'tomatoes', 'bananas', 'baking soda']

RECIPES = {
    'Pancakes': ['flour', 'sugar', 'salt', 'eggs', 'milk', 'butter'],
    'Omelette': ['eggs', 'butter', 'salt', 'milk'],
    'Sugar Cookies': ['flour', 'sugar', 'butter', 'eggs'],
    'Chocolate Cake': ['flour', 'sugar', 'salt', 'eggs', 'milk', 'butter', 'cocoa powder', 'baking powder', 'vanilla extract'],
    'Spaghetti Carbonara': ['spaghetti', 'pancetta', 'eggs', 'parmigiano reggiano', 'pecorino romano', 'black pepper', 'salt'],
    'Banana Bread': ['flour', 'sugar', 'butter', 'bananas', 'eggs', 'baking soda', 'vanilla extract'],
    'Tomato Soup': ['tomatoes', 'onion', 'garlic', 'chicken or vegetable broth', 'olive oil', 'sugar', 'salt', 'pepper'],
    'Roast Chicken': ['whole chicken', 'butter', 'garlic', 'lemon', 'salt', 'pepper', 'thyme'],
}

def check_recipes():
    available_ingredients = [INGREDIENTS[i] for i in range(len(INGREDIENTS)) if ingredient_vars[i].get() == 1]
    selected_food_types = [food_type_var.get()] if food_type_var.get() else FOOD_TYPES
    compatible_recipes = []
    for recipe, details in RECIPES.items():
        if set(details['ingredients']).issubset(set(available_ingredients)) and details['type'] in selected_food_types:
            compatible_recipes.append(recipe)
    if compatible_recipes:
        recipe_label.config(text=f"Compatible recipes: {', '.join(compatible_recipes)}")
    else:
        closest_match = max(RECIPES.keys(), key=lambda x: SequenceMatcher(None, x, ''.join(available_ingredients)).ratio())
        missing_ingredients = set

root = Tk()
root.title("Recipe Finder")
root.geometry ("500x300")

ingredient_vars = []
for i in range(len(INGREDIENTS)):
    var = IntVar()
    checkbox = Checkbutton(root, text=INGREDIENTS[i], variable=var)
    checkbox.grid(row=i, column=0, sticky=W)
    ingredient_vars.append(var)

button = Button(root, text="Check Recipes", command=check_recipes)
button.grid(row=len(INGREDIENTS), column=0, columnspan=2)

recipe_label = Label(root, text="")
recipe_label.grid(row=len(INGREDIENTS)+1, column=0, columnspan=2)

root.mainloop()



#pievienot tabu, kur pievienot savas receptes un ingredientes
#pievienot = Tk()
root.title("Recipe Finder")

# Ingredient checkboxes
ingredient_vars = []
for i in range(len(INGREDIENTS)):
    var = IntVar()
checkbox = Checkbutton(root, text=INGREDIENTS[i], variable=var)
checkbox.grid(row=i, column=0, sticky=W)
ingredient_vars.append(var)

button = Button(root, text="Check Recipes", command=check_recipes)
button.grid(row=len(INGREDIENTS), column=0, columnspan=2)

recipe_label = Label(root, text="")
recipe_label.grid(row=len(INGREDIENTS)+1, column=0, columnspan=2)

root.mainloop()