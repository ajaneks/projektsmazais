from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar
import datetime
import customtkinter

# Objekta izveide
# root = Tk()
root = customtkinter.CTk()

root.geometry("400x600")

customtkinter.set_appearance_mode("system")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


# Iegut sodienas datumu
today = datetime.datetime.today()

# notebook = ttk.Notebook(root)
# notebook.pack(fill = BOTH, expand = True)

# # Kalendara tabs
# calendar_tab = ttk.Frame(notebook)
# notebook.add(calendar_tab, text = "Calendar")

# # Komentaru tabs
# comments_tab = ttk.Frame(notebook)
# notebook.add(comments_tab, text = "Comments")

def grad_date(event):
    selected_date = cal.get_date()
    if selected_date in comments:
        comment = comments[selected_date]
    else:
        comment = "No comment for this date."
    date.config(text = "Selected Date is: " + selected_date + "\nComment: " + comment)

# Create the calendar
calendar_frame = Frame(root)
calendar_frame.pack(side=LEFT, fill=BOTH, expand=True)
cal = Calendar(calendar_frame, selectmode='day', year=today.year, month=today.month, day=today.day)
cal.pack(pady=20)
cal.bind("<<CalendarSelected>>", grad_date)

# Create the comments section
comments_frame = Frame(root)
comments_frame.pack(side=RIGHT, fill=BOTH, expand=True)

def display_comments():
    comments_list.delete(0, END)
    for date, comment in comments.items():
        comments_list.insert(END, date + ": " + comment)

# comments_list = Listbox(comments_frame)
# comments_list.pack(fill=BOTH, expand=True)




# # Kalendara pievienosana
# cal = Calendar(calendar_tab, selectmode = 'day', year = today.year, month = today.month, day = today.day)
# cal.pack(pady = 20)
# cal.bind("<<CalendarSelected>>", grad_date)

# Komentaru un datumu vieta
comments = {}


def add_comment():
    selected_date = cal.get_date()
    comment = comment_entry.get()
    comments[selected_date] = comment
    comment_entry.delete(0, END)
    date.config(text = "Selected Date is: " + selected_date + "\nComment: " + comment)
    display_comments()

def remove_comment():
    selected_date = cal.get_date()
    if selected_date in comments:
        del comments[selected_date]
        date.config(text = "Comment removed for: " + selected_date)
        display_comments()
    else:
        date.config(text = "No comment to remove for: " + selected_date)

# Pogas
customtkinter.CTkButton(calendar_frame, text = "Add Comment", command = add_comment).pack(pady = 20)
customtkinter.CTkButton(calendar_frame, text = "Remove Comment", command = remove_comment).pack(pady = 20)

segemented_button_var = customtkinter.StringVar(value="Kalendārs")
segemented_button_var = customtkinter.StringVar(value="Plāni")  # set initial value

segemented_button = customtkinter.CTkSegmentedButton(master=root,
                                                     values=["Kalendārs","Plāni"],
                                                     variable=segemented_button_var)
segemented_button.pack(padx=20, pady=10)

# button = customtkinter.CTkButton(master=root, text="Get Date", command=grad_date)
# button.place(relx=0.5, rely=0.5)

comment_entry = Entry(calendar_frame)
comment_entry.pack(pady = 20)

date = Label(calendar_frame, text = "")
date.pack(pady = 20)

# Kaste, kur uzradas komentari
def display_comments():
    comments_list.delete(0, END)
    for date, comment in comments.items():
        comments_list.insert(END, date + ": " + comment)

comments_list = Listbox(comments_frame)
comments_list.pack(fill = BOTH, expand = True)


root.mainloop()
