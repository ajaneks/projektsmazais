from tkinter import *
from difflib import SequenceMatcher

# List of ingredients and recipes
INGREDIENTS = ['flour', 'sugar', 'salt', 'eggs', 'milk', 'butter']
RECIPES = {
    'Pancakes': ['flour', 'sugar', 'salt', 'eggs', 'milk', 'butter'],
    'Omelette': ['eggs', 'butter', 'salt', 'milk'],
    'Sugar Cookies': ['flour', 'sugar', 'butter', 'eggs']
}

# Function to check compatible recipes
def check_recipes():
    available_ingredients = [INGREDIENTS[i] for i in range(len(INGREDIENTS)) if ingredient_vars[i].get() == 1]
    compatible_recipes = []
    for recipe, ingredients in RECIPES.items():
        if set(ingredients).issubset(set(available_ingredients)):
            compatible_recipes.append(recipe)
    if compatible_recipes:
        recipe_label.config(text=f"Compatible recipes: {', '.join(compatible_recipes)}")
    else:
        closest_match = max(RECIPES.keys(), key=lambda x: SequenceMatcher(None, x, ''.join(available_ingredients)).ratio())
        missing_ingredients = list(set(RECIPES[closest_match]) - set(available_ingredients))
        recipe_label.config(text=f"No compatible recipes found. Closest match: {closest_match}. Missing ingredients: {', '.join(missing_ingredients)}")

# Tkinter GUI
root = Tk()
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