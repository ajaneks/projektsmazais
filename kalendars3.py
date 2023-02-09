from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar
import datetime

# Create Object
root = Tk()

# Set geometry
root.geometry("400x400")

# Get today's date
today = datetime.datetime.today()

# Add Notebook
notebook = ttk.Notebook(root)
notebook.pack(fill = BOTH, expand = True)

# Add Calendar Tab
calendar_tab = ttk.Frame(notebook)
notebook.add(calendar_tab, text = "Calendar")

# Add Comments Tab
comments_tab = ttk.Frame(notebook)
notebook.add(comments_tab, text = "Comments")

def grad_date(event):
    selected_date = cal.get_date()
    if selected_date in comments:
        comment = comments[selected_date]
    else:
        comment = "No comment for this date."
    date.config(text = "Selected Date is: " + selected_date + "\nComment: " + comment)


# Add Calendar
cal = Calendar(calendar_tab, selectmode = 'day', year = today.year, month = today.month, day = today.day)
cal.pack(pady = 20)
cal.bind("<<CalendarSelected>>", grad_date)

# Dictionary to store date and comment
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

# Add Button and Label
Button(calendar_tab, text = "Add Comment", command = add_comment).pack(pady = 20)
Button(calendar_tab, text = "Remove Comment", command = remove_comment).pack(pady = 20)

comment_entry = Entry(calendar_tab)
comment_entry.pack(pady = 20)

date = Label(calendar_tab, text = "")
date.pack(pady = 20)

# Add Listbox to display comments
def display_comments():
    comments_list.delete(0, END)
    for date, comment in comments.items():
        comments_list.insert(END, date + ": " + comment)

comments_list = Listbox(comments_tab)
comments_list.pack(fill = BOTH, expand = True)

# Execute Tkinter
root.mainloop()
