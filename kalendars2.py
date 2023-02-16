from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar
import datetime
import customtkinter
from tkinter import Toplevel



# Objekta izveide
root = customtkinter.CTk()
root.title("Plānotājs")
root.geometry("500x600")

#Customtkinter stils
customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

# Iegut sodienas datumu
today = datetime.datetime.today()

def grad_date(event):
    selected_date = cal.get_date()
    if selected_date in comments:
        comment = comments[selected_date]
        # Set background color to yellow for dates with comments
        cal.tag_config(selected_date, background='yellow')
    else:
        comment = "Šajā datumā nav plānu."
        # Set default background color for dates without comments
        cal.tag_config(selected_date, background='white')
    date.config(text = "Izvēlētais datums ir: " + selected_date + "\nPlāni: " + comment)

# Kalendāra izveide, stila mainīšana
calendar_frame = Frame(root, bg='#f1f1f1', bd=2, relief='groove')
calendar_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

cal = Calendar(calendar_frame, selectmode='day', year=today.year, month=today.month, day=today.day,
               background='#f1f1f1', foreground='black', font=('Arial', 10), 
               borderwidth=0, headersbackground='#4a90e2', normalbackground='#f1f1f1',
               weekendbackground='#f1f1f1', selectbackground='#4a90e2')
cal.pack(pady=20)

cal.bind("<<CalendarSelected>>", grad_date)



# Create the comments section
comments_frame = Frame(root)
comments_frame.pack(side=RIGHT, fill=BOTH, expand=True)

# Kaste, kur uzradas komentari
comments_list = Listbox(comments_frame)
comments_list.pack(fill = BOTH, expand = True)


def display_comments():
    comments_list.delete(0, END)
    for date, comment in comments.items():
        comments_list.insert(END, date + ": " + comment)

# Komentaru un datumu vieta
comments = {}

for date in comments.keys():
    cal.tag_config(date, background='yellow')

# Save comments to file
def save_comments():
    with open('comments.txt', 'w') as file:
        for date, comment in comments.items():
            file.write(f'{date}:{comment}\n')

# Load comments from file
def load_comments():
    try:
        with open('comments.txt', 'r') as file:
            for line in file:
                date, comment = line.strip().split(':')
                comments[date] = comment
    except FileNotFoundError:
        pass

load_comments() # load saved comments on startup
display_comments() # display comments on startup

def add_comment():
    selected_date = cal.get_date()
    comment = comment_entry.get()
    comments[selected_date] = comment
    comment_entry.delete(0, END)
    date.config(text = "Izvēlētais datums ir: " + selected_date + "\nPlāni: " + comment)
    display_comments()
    # Set background color to yellow for dates with comments
    cal.tag_config(selected_date, background='yellow')
    save_comments() # save comments after adding

def remove_comment():
    selected_date = cal.get_date()
    if selected_date in comments:
        del comments[selected_date]
        date.config(text = "Noņemt plānu no: " + selected_date)
        display_comments()
        # Set default background color for dates without comments
        cal.tag_config(selected_date, background='white')
        save_comments() # save comments after removing
    else:
        date.config(text = "Šajā datumā nav plānu: " + selected_date)

def set_recurring_event():
    # Create a new window for setting the recurring event
    recurring_window = Toplevel(root)
    recurring_window.title("Set recurring event")
    recurring_window.geometry("400x500")

    # Add labels and entry boxes for the event details
    event_name_label = Label(recurring_window, text="Event name:")
    event_name_label.pack(pady=10)
    event_name_entry = Entry(recurring_window)
    event_name_entry.pack()

    start_date_label = Label(recurring_window, text="Start date:")
    start_date_label.pack(pady=10)
    start_date_entry = Calendar(recurring_window, selectmode='day', year=today.year, month=today.month, day=today.day)
    start_date_entry.pack()

    frequency_label = Label(recurring_window, text="Frequency (days):")
    frequency_label.pack(pady=10)
    frequency_entry = Entry(recurring_window)
    frequency_entry.pack()

    # Add a function to handle saving the recurring event
    def save_recurring_event():
        event_name = event_name_entry.get()
        start_date = start_date_entry.get_date()
        frequency = int(frequency_entry.get())

        # Add the first event to the calendar
        comments[start_date] = event_name
        cal.tag_config(start_date, background='yellow')

        # Add the recurring events to the calendar
        current_date = datetime.datetime.strptime(start_date, '%m/%d/%y')
        while current_date < datetime.datetime.today() + datetime.timedelta(days=365):
            current_date += datetime.timedelta(days=frequency)
            comments[current_date.strftime('%m/%d/%y')] = event_name
            cal.tag_config(current_date.strftime('%m/%d/%y'), background='yellow')

        # Update the comments list and save the comments to file
        display_comments()
        save_comments()

        # Close the recurring event window
        recurring_window.destroy()

    # Add a button to save the recurring event
    customtkinter.CTkButton(recurring_window, text="Save", command=save_recurring_event).pack(pady=20)


# Pogas
customtkinter.CTkButton(calendar_frame, text = "Pievienot plānu", command = add_comment).pack(pady = 20)
customtkinter.CTkButton(calendar_frame, text = "Dzēst plānu", command = remove_comment).pack(pady = 20)
customtkinter.CTkButton(calendar_frame, text="Set recurring event", command=set_recurring_event).pack(pady=20)

comment_entry = Entry(calendar_frame)
comment_entry.pack(pady = 20)

date = Label(calendar_frame, text = "")
date.pack(pady = 20)

root.mainloop()