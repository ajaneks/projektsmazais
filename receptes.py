from tkinter import *
from tkinter import ttk
from difflib import SequenceMatcher 

INGREDIENTS = ['flour', 'sugar', 'salt', 'eggs', 'milk', 'butter', 'cocoa powder', 'baking powder', 'vanilla extract', 'spaghetti', 'pancetta', 'parmigiano reggiano', 'pecorino romano', 'black pepper', 'onion', 'garlic', 'chicken or vegetable broth', 'olive oil', 'sugar', 'pepper', 'whole chicken', 'lemon', 'thyme', 'tomatoes', 'bananas', 'baking soda']

RECIPES = {
    'Pancakes': ['flour', 'sugar', 'salt', 'eggs', 'milk', 'butter'],
    'Omelette': ['eggs', 'butter', 'salt', 'milk'],
}

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
        missing_ingredients = set(RECIPES[closest_match]) - set(available_ingredients)
        recipe_label.config(text=f"No compatible recipes found. \nClosest match: {closest_match}. \nMissing ingredients: {', '.join(missing_ingredients)}")

    


root = Tk()
root.title("Recipe Finder")
root.geometry ("500x300")

def add_recipe_window():
    add_recipe = Toplevel(root)
    add_recipe.title("Add Recipe")
    add_recipe.geometry("400x300")

    recipe_name_label = Label(add_recipe, text="Recipe Name:")
    recipe_name_label.pack()

    recipe_name_entry = Entry(add_recipe)
    recipe_name_entry.pack()

    scrollbar = ttk.Scrollbar(add_recipe)
    scrollbar.pack(side=RIGHT, fill=Y)

    ingredients_frame = Frame(add_recipe)
    ingredients_frame.pack(fill=BOTH, expand=True)

    ingredient_vars = []
    for i in range(len(INGREDIENTS)):
        var = IntVar()
        checkbox = Checkbutton(ingredients_frame, text=INGREDIENTS[i], variable=var)
        checkbox.pack(anchor=W)
        ingredient_vars.append(var)

    ingredients_frame.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=ingredients_frame.yview)

    add_recipe_button = Button(add_recipe, text="Add Recipe", command=lambda: add_recipe_to_list(recipe_name_entry.get(), ingredient_vars,add_recipe))
    add_recipe_button.pack()

    add_recipe.mainloop()

add_recipe_button = Button(root, text="Add Recipe", command=add_recipe_window)
add_recipe_button.grid(row=len(INGREDIENTS)+2, column=0, columnspan=2)

def add_recipe_to_list(recipe_name, ingredient_vars,add_recipe):
    new_recipe_ingredients = [INGREDIENTS[i] for i in range(len(INGREDIENTS)) if ingredient_vars[i].get() == 1]
    RECIPES[recipe_name] = new_recipe_ingredients
    add_recipe.destroy()



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

