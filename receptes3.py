import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image, ImageTk

# Sample recipe data
recipes = {
    "Pasta": {"pasta", "tomato sauce", "olive oil", "garlic", "salt", "pepper"},
    "Grilled Cheese": {"bread", "butter", "cheese"},
}

#klase prieks ikonas
class CustomCTk(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.iconbitmap("")

class RecipeApp(CustomCTk):
    def __init__(self):
        super().__init__()

        self.configure(bg="white")  # Set the background color of the main window
        self.title("Recipe Generator")

        
        self.side_buttons = ttk.Frame(self)
        self.side_buttons.pack(side="left", fill="y")

        image = Image.open("lasagna2.png")
        resized_image = image.resize((150, 150), Image.ANTIALIAS)
        self.logo_image = ImageTk.PhotoImage(resized_image)
        self.logo_label = tk.Label(self.side_buttons, image=self.logo_image, bg="white")
        self.logo_label.pack(pady=(10, 20), anchor="center")

        icon_image = resized_image.copy()
        self.icon_photo = ImageTk.PhotoImage(icon_image)
        self.iconphoto(True, self.icon_photo)

        self.home_button = ctk.CTkButton(self.side_buttons, text="Home", command=lambda: self.notebook.select(self.tab1), corner_radius=5)
        self.home_button.pack(fill="x", padx=5, pady=5)

        self.ingredient_check_button = ctk.CTkButton(self.side_buttons, text="Ingredient Check", command=lambda: self.notebook.select(self.tab2),corner_radius=5)
        self.ingredient_check_button.pack(fill="x", padx=5, pady=5)

        self.add_recipe_button = ctk.CTkButton(self.side_buttons, text="Add Recipe", command=lambda: self.notebook.select(self.tab3), corner_radius=5)
        self.add_recipe_button.pack(fill="x", padx=5, pady=5)

        # Create a custom style for the notebook
        style = ttk.Style()
        style.configure("Hidden.TNotebook", tabmargins=0)
        style.layout("Hidden.TNotebook.Tab", [])

        self.notebook = ttk.Notebook(self, style="Hidden.TNotebook")
        self.notebook.pack(side="left", fill="both", expand=True)
        
        self.tab1 = Home(self.notebook)
        self.tab2 = IngredientCheck(self.notebook)
        self.tab3 = AddRecipe(self.notebook)

        self.notebook.add(self.tab1, text="Home")
        self.notebook.add(self.tab2, text="Ingredient Check")
        self.notebook.add(self.tab3, text="Add Recipe")



class Home(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.welcome_label = ttk.Label(self, text="Welcome to the Recipe Generator!", font=("Arial", 16))
        self.welcome_label.pack(pady=20)

        self.description_label = ttk.Label(self, text="Select the ingredients you have, and we'll generate a recipe for you.\n\nYou can also add your own recipes!", wraplength=300)
        self.description_label.pack(pady=20)


class IngredientCheck(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.check_boxes = []
        self.ingredients_list = sorted(set.union(*recipes.values()))

        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.check_boxes_frame = ttk.Frame(self.canvas)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.create_window((0, 0), window=self.check_boxes_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        for index, ingredient in enumerate(self.ingredients_list):
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(self.check_boxes_frame, text=ingredient, variable=var)
            chk.grid(row=index, column=0, sticky="W")
            self.check_boxes.append((chk, var))

        self.check_boxes_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.generate_button = ctk.CTkButton(self, text="Generate Recipe", command=self.generate_recipe)
        self.generate_button.grid(row=1, column=0, pady=10)

        self.result = ttk.Label(self, text="", wraplength=300)  # Set the wraplength to your desired value
        self.result.grid(row=2, column=0, pady=10)

    def generate_recipe(self):
        selected_ingredients = [chk["text"] for chk, var in self.check_boxes if var.get()]

        if not selected_ingredients:
            self.result.config(text="No ingredients selected. Please select at least one ingredient.")
            return

        possible_recipes = []

        for recipe, ingredients in recipes.items():
            if set(selected_ingredients).issuperset(ingredients):
                possible_recipes.append(recipe)

        if possible_recipes:
            self.result["text"] = "Recipes: " + ", ".join(possible_recipes)
        else:
            self.result["text"] = self.closest_recipe(selected_ingredients)



    def closest_recipe(self, selected_ingredients):
        min_missing_count = float('inf')
        closest_recipe = None
        missing_ingredients = None

        for recipe, ingredients in recipes.items():
            missing = ingredients - set(selected_ingredients)
            missing_count = len(missing)

            if missing_count < min_missing_count:
                min_missing_count = missing_count
                closest_recipe = recipe
                missing_ingredients = missing

        return f"Closest recipe: {closest_recipe}. Missing ingredients: {', '.join(missing_ingredients)}"

    def update_ingredient_checkboxes(self):
        self.ingredients_list = sorted(set.union(*recipes.values()))

        for chk, _ in self.check_boxes:
            chk.grid_remove()

        self.check_boxes = []

        for index, ingredient in enumerate(self.ingredients_list):
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(self.check_boxes_frame, text=ingredient, variable=var)
            chk.grid(row=index, column=0, sticky="W")
            self.check_boxes.append((chk, var))

        self.check_boxes_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

class AddRecipe(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.recipe_name_label = ttk.Label(self, text="Recipe Name")
        self.recipe_name_label.grid(row=0, column=0, padx=(10, 0), pady=(10, 0))

        self.recipe_name_entry = ttk.Entry(self)
        self.recipe_name_entry.grid(row=0, column=1, padx=10, pady=(10, 0))

        self.ingredients_label = ttk.Label(self, text="Ingredients (comma-separated)")
        self.ingredients_label.grid(row=1, column=0, padx=(10, 0), pady=(10, 0))

        self.ingredients_entry = ttk.Entry(self)
        self.ingredients_entry.grid(row=1, column=1, padx=10, pady=(10, 0))

        self.add_recipe_button = ctk.CTkButton(self, text="Add Recipe", command=self.add_recipe)
        self.add_recipe_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.result = ttk.Label(self, text="", wraplength=300)  # Set the wraplength to your desired value
        self.result.grid(row=3, column=0, columnspan=2, pady=10)

    def add_recipe(self):
        recipe_name = self.recipe_name_entry.get().strip()
        ingredients = set(map(str.strip, self.ingredients_entry.get().split(',')))

        if recipe_name and ingredients:
            recipes[recipe_name] = ingredients
            self.result["text"] = f"{recipe_name} added successfully!"

            # Update ingredient checkboxes
            ingredient_check_tab = self.master.nametowidget(self.master.tabs()[1])
            ingredient_check_tab.update_ingredient_checkboxes()
        else:
            self.result["text"] = "Please enter a valid recipe name and ingredients."


def main():
    app = RecipeApp()
    app.mainloop()
if __name__ == "__main__":
    main()