import tkinter as tk
from tkinter import messagebox
import random

# list of meals
meals = ["Chicken Fajitas", "Pasta Carbonara", "Beef Stir Fry", "Vegetable Curry", "Tofu Scramble"]

# function to generate meal plan
def generate_meal_plan():
    # get user input for number of meals and days
    num_meals = num_meals_entry.get()
    num_days = num_days_entry.get()

    # validate user input
    if not num_meals.isdigit() or not num_days.isdigit():
        messagebox.showerror("Error", "Please enter valid numbers for meals and days")
        return

    num_meals = int(num_meals)
    num_days = int(num_days)

    if num_meals < 1 or num_days < 1:
        messagebox.showerror("Error", "Please enter a positive number for meals and days")
        return

    # clear previous meal plan
    meal_plan_list.delete(0, tk.END)

    # generate meal plan
    for day in range(1, num_days+1):
        meal_plan_list.insert(tk.END, f"Day {day}:")
        for i in range(num_meals):
            meal = random.choice(meals)
            meal_plan_list.insert(tk.END, f"  {i+1}. {meal}")

# create main window
root = tk.Tk()
root.title("Meal Planner")

# create labels
tk.Label(root, text="Number of Meals per Day:").grid(row=0, column=0, pady=5, padx=10, sticky="w")
tk.Label(root, text="Number of Days:").grid(row=1, column=0, pady=5, padx=10, sticky="w")

# create entry fields
num_meals_entry = tk.Entry(root, width=5)
num_meals_entry.grid(row=0, column=1, pady=5, padx=10)
num_days_entry = tk.Entry(root, width=5)
num_days_entry.grid(row=1, column=1, pady=5, padx=10)

# create meal plan listbox
meal_plan_list = tk.Listbox(root, height=10, width=50)
meal_plan_list.grid(row=2, column=0, columnspan=2, pady=10, padx=10)

# create generate button
generate_button = tk.Button(root, text="Generate Meal Plan", command=generate_meal_plan)
generate_button.grid(row=3, column=0, pady=10, padx=10, sticky="w")

# create exit button
exit_button = tk.Button(root, text="Exit", command=root.quit)
exit_button.grid(row=3, column=1, pady=10, padx=10, sticky="e")

root.mainloop()
