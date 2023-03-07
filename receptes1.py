 #In this version, we use the `SequenceMatcher` class from the `difflib` module to find the closest matching recipe. We first create a list of available ingredients, as before. If no compatible recipes are found, we use the `max()` function to find the key in the `RECIPES` dictionary with the highest matching ratio to the available ingredients. The matching ratio is calculated using the `SequenceMatcher` class, which compares the available ingredients to each recipe name and returns a value between 0 and 1 indicating the similarity. When the program is run and no compatible recipes are found, the user will see a message indicating the closest matching recipe based on their available ingredients.

from tkinter import *
from difflib import SequenceMatcher 
import customtkinter


customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

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
    compatible_recipes = []
    for recipe, ingredients in RECIPES.items():
        if set(ingredients).issubset(set(available_ingredients)):
            compatible_recipes.append(recipe)
    if compatible_recipes:
        recipe_label.configure(text=f"Compatible recipes: {', '.join(compatible_recipes)}")
    else:
        closest_match = max(RECIPES.keys(), key=lambda x: SequenceMatcher(None, x, ''.join(available_ingredients)).ratio())
        missing_ingredients = set(RECIPES[closest_match]) - set(available_ingredients)
        recipe_label.configure(text=f"No compatible recipes found. \nClosest match: {closest_match}. \nMissing ingredients: {', '.join(missing_ingredients)}")

    


root = customtkinter.CTk()
root.title("Recipe Finder")
root.geometry ("400x800")

def add_recipe_window():
    add_recipe = Toplevel(root)
    add_recipe.title("Add Recipe")
    add_recipe.geometry("400x800")

    recipe_name_label = customtkinter.CTkLabel(add_recipe, text="Recipe Name:")
    recipe_name_label.pack()

    recipe_name_entry = customtkinter.CTkEntry(add_recipe)
    recipe_name_entry.pack()

    ingredient_vars = []
    for i in range(len(INGREDIENTS)):
        var = IntVar()
        checkbox = customtkinter.CTkCheckBox(add_recipe, text=INGREDIENTS[i], variable=var)
        checkbox.pack(anchor=W)
        ingredient_vars.append(var)

    add_recipe_button = customtkinter.CTkButton(add_recipe, text="Add Recipe", command=lambda: add_recipe_to_list(recipe_name_entry.get(), ingredient_vars,add_recipe))
    add_recipe_button.pack()

    add_recipe.mainloop()

add_recipe_button = customtkinter.CTkButton(root, text="Add Recipe", command=add_recipe_window)
add_recipe_button.grid(row=len(INGREDIENTS)+2, column=0, columnspan=2)

def add_recipe_to_list(recipe_name, ingredient_vars,add_recipe):
    new_recipe_ingredients = [INGREDIENTS[i] for i in range(len(INGREDIENTS)) if ingredient_vars[i].get() == 1]
    RECIPES[recipe_name] = new_recipe_ingredients
    add_recipe.destroy()


ingredient_vars = []
for i in range(len(INGREDIENTS)):
    var = IntVar()
    checkbox = customtkinter.CTkCheckBox(root, text=INGREDIENTS[i], variable=var)
    checkbox.grid(row=i, column=0, sticky=W)
    ingredient_vars.append(var)

button = customtkinter.CTkButton(root, text="Check Recipes", command=check_recipes)
button.grid(row=len(INGREDIENTS), column=0, columnspan=2)

recipe_label = customtkinter.CTkLabel(root, text="")
recipe_label.grid(row=len(INGREDIENTS)+1, column=0, columnspan=2)

root.mainloop()



#pievienot tabu, kur pievienot savas receptes un ingredientes
#pievienot 