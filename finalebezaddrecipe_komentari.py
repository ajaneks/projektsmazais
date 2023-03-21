import tkinter as tk  # Importējam tkinter bibliotēku un piešķiram tai "tk" saīsinājumu
from tkinter import ttk  # Importējam ttk no tkinter bibliotēkas
import customtkinter as ctk  # Importējam customtkinter bibliotēku un piešķiram tai "ctk" saīsinājumu
from PIL import Image, ImageTk  # Importējam Image un ImageTk bibliotēkas no PIL bibliotēkas

def load_recipes(file_name):
    recipes = {}  # Izveidojam tukšu vārdnīcu, lai glabātu receptes
    with open(file_name, "r") as file:  # Atveram failu lasīšanai
        for line in file:  # Katrā faila rindā
            line = line.strip()  # Noņemam pārākumus no rindas sākuma un beigām
            if line:  # Ja rinda nav tukša
                recipe_data, instructions = line.split("|")  # Atdalām receptes datus un instrukcijas
                recipe_name, ingredients_str = recipe_data.split(":")  # Atdalām receptes nosaukumu un sastāvdaļas
                ingredients = set(map(str.strip, ingredients_str.split(",")))  # Atdalām atsevišķas sastāvdaļas, noņemot atstarpes, un ievietojam kā kopa
                recipes[recipe_name] = (ingredients, instructions)  # Pievienojam vārdnīcai recepti ar tās nosaukumu kā atslēgu, sastāvdaļām un instrukcijām kā vērtību
    return recipes  # Atgriežam visas ielasītās receptes vārdnīcas formātā


# Ielādējam receptes no teksta faila
recipes = load_recipes("recipes.txt")

# Klase ikonai
class CustomCTk(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.iconbitmap("")

class RecipeApp(CustomCTk):
    def __init__(self):
        super().__init__()

        self.configure(bg="white")  # Iestatām fona krāsu uz baltu
        self.title("Recipe Generator")  # Iestatām loga virsrakstu uz "Recipe Generator"


        # Izveidojam loga kreisās puses pogas
        self.side_buttons = ttk.Frame(self)
        self.side_buttons.pack(side="left", fill="y")

        # Ielādējam logo un iestatām to kā  attēlu
        image = Image.open("lasagna2.png")
        resized_image = image.resize((150, 150), Image.ANTIALIAS)
        self.logo_image = ImageTk.PhotoImage(resized_image)
        self.logo_label = tk.Label(self.side_buttons, image=self.logo_image, bg="white")
        self.logo_label.pack(pady=(10, 20), anchor="center")

        icon_image = resized_image.copy()
        self.icon_photo = ImageTk.PhotoImage(icon_image)
        self.iconphoto(True, self.icon_photo)

        # izveido pirmo pogu "Home"
        self.home_button = ctk.CTkButton(self.side_buttons, text="Home", command=lambda: self.notebook.select(self.tab1), corner_radius=5)
        self.home_button.pack(fill="x", padx=5, pady=5)

        # izveido otro pogu "Ingredient Check"
        self.ingredient_check_button = ctk.CTkButton(self.side_buttons, text="Ingredient Check", command=lambda: self.notebook.select(self.tab2),corner_radius=5)
        self.ingredient_check_button.pack(fill="x", padx=5, pady=5)

        # uzstāda notebook izkārtojumu
        style = ttk.Style()
        style.configure("Hidden.TNotebook", tabmargins=0)
        style.layout("Hidden.TNotebook.Tab", [])

        # izveido notebook
        self.notebook = ttk.Notebook(self, style="Hidden.TNotebook")
        self.notebook.pack(side="left", fill="both", expand=True)
        self.tab1 = Home(self.notebook)
        self.tab2 = IngredientCheck(self.notebook)

        # pievieno tabus notebookam
        self.notebook.add(self.tab1, text="Home")
        self.notebook.add(self.tab2, text="Ingredient Check")
   

class Home(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        # Sasveicinās
        self.welcome_label = ttk.Label(self, text="Welcome to the Recipe Generator!", font=("Arial", 16))
        self.welcome_label.pack(pady=20)
        # Programmas apraksts
        self.description_label = ttk.Label(self, text="Select the ingredients you have, and we'll generate a recipe for you.\n", wraplength=300)
        self.description_label.pack(pady=20)

#apakšklase, kas atbild par iespējamo sastāvdaļu izvēli
class IngredientCheck(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        # saglabā izvēlēto ēdienu kastītes
        self.check_boxes = []
        # izveido sarakstu ar iespējamo sastāvdaļu sarakstiem
        self.ingredients_list = sorted(set.union(*(ingredients for ingredients, _ in recipes.values())))

         # izveido kanvu un scrollbar, lai rādītu izvēlēto sastāvdaļu sarakstu, kad saraksts ir pārāk garš
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.check_boxes_frame = ttk.Frame(self.canvas)

        # izvieto kanvu un scrollbar, un saglabā izvēlētās sastāvdaļas
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.create_window((0, 0), window=self.check_boxes_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # izveido iespējamo sastāvdaļu kastītes un pievieno tos kanvai un sarakstam
        for index, ingredient in enumerate(self.ingredients_list):
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(self.check_boxes_frame, text=ingredient, variable=var)
            chk.grid(row=index, column=0, sticky="W")
            self.check_boxes.append((chk, var))

        # atjaunina kanvu un sarakstu
        self.check_boxes_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        # konfigurē rindas un kolonnas
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # izveido pogu "Generate recipe" un laukumu ar atbildi
        self.generate_button = ctk.CTkButton(self, text="Generate Recipe", command=self.generate_recipe)
        self.generate_button.grid(row=1, column=0, pady=10)

        self.result_frame = ttk.Frame(self)
        self.result_frame.grid(row=2, column=0, pady=10)

        # izveido teksta lauku, kurā rādīsies atbilde
        self.result = tk.Text(self.result_frame, wrap=tk.WORD, width=40, height=10, state='disabled')
        self.result.pack(side="left", fill="both")
        # izveido scrollbaru, ja atbilde ir pārāk gara
        self.result_scrollbar = ttk.Scrollbar(self.result_frame, orient="vertical", command=self.result.yview)
        self.result_scrollbar.pack(side="right", fill="y")
        self.result.config(yscrollcommand=self.result_scrollbar.set, bg="white") 

    def generate_recipe(self):
        # Izvelk atzīmētos
        selected_ingredients = [chk["text"] for chk, var in self.check_boxes if var.get()]
        # Ja nav atlasīti nekādi produkti
        if not selected_ingredients:
            self.result.config(text="No ingredients selected. Please select at least one ingredient.")
            return
        
        # Visas iespejamās receptes
        possible_recipes = []

        for recipe, recipe_data in recipes.items():
            # izvelk receptes sastāvdaļas un instrukcijas
            ingredients, instructions = recipe_data
            # ja sastāvdaļas ir apvienojamas ar atlasītajiem produktiem
            if set(selected_ingredients).issuperset(ingredients):
                possible_recipes.append((recipe, instructions))

        if possible_recipes:
            # ja ir iespejamās receptes
            # saraksta formatēšana
            result_text = "\n".join([f"{recipe}: {instructions}" for recipe, instructions in possible_recipes])
            # atjauno rezultāta tekstu
            self.update_result_text("Recipes:\n" + result_text)
        else:
            # ja nav iespejamās receptes
            # iegūt tuvāko recepti
            self.update_result_text(self.closest_recipe(selected_ingredients))

    def update_result_text(self, text):
        # atjauno resultata tekstu
        self.result.config(state='normal')
        self.result.delete(1.0, tk.END)
        self.result.insert(tk.END, text)
        self.result.config(state='disabled')


    def closest_recipe(self, selected_ingredients):
        # inicializē lielāko sakritību un mazāko trūkstošo produktu skaitu
        max_matching_count = -1
        min_missing_count = float('inf')
        closest_recipe = None
        missing_ingredients = None

        for recipe, recipe_data in recipes.items(): 
            # izvelk receptes sastāvdaļas
            ingredients, _ = recipe_data
            # iegūt trūkstošos produktus  
            missing = ingredients - set(selected_ingredients)
            missing_count = len(missing)
            matching_count = len(ingredients) - missing_count

            if matching_count > max_matching_count or (matching_count == max_matching_count and missing_count < min_missing_count):
                # ja ir lielāka sakritība vai vienāda sakritība ar mazāku trūkstošo produktu skaitu, tad piešķir lielāko sakritību un mazāko trūkstošo produktu skaitu
                max_matching_count = matching_count
                min_missing_count = missing_count
                #tuvākā recepte un trūkstošie produkti
                closest_recipe = recipe
                missing_ingredients = missing
        #Izvada tuvāko recepti, trūsktošos produktus
        return f"Closest recipe: {closest_recipe}. Missing ingredients: {', '.join(missing_ingredients)}"


def main():
    app = RecipeApp()
    app.mainloop()
if __name__ == "__main__":
    main()