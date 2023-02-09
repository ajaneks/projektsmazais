# Import Required Library
from tkinter import *
from tkcalendar import Calendar
from tkcalendar import DateEntry
import customtkinter


customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

# Create Object
root = customtkinter.CTk()

# Set geometry
root.geometry("400x400")

root.configure('my.DateEntry',
                fieldbackground='light green',
                background='dark green',
                foreground='dark blue',
                arrowcolor='white')

# Add Calendar
cal = Calendar(root, selectmode = 'day',
			year = 2020, month = 5,
			day = 22)

cal.pack(pady = 20)

def grad_date():
	date.config(text = "Selected Date is: " + cal.get_date())

# Add Button and Label
# Button(root, text = "Get Date",
# 	command = grad_date).pack(pady = 20)

button = customtkinter.CTkButton(master=root, text="Get Date", command=grad_date)
button.place(relx=0.5, rely=0.5)


date = Label(root, text = "")
date.pack(pady = 20)

# Execute Tkinter
root.mainloop()
