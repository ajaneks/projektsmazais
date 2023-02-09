root = Tk()
root.geometry("400x600")

# Get today's date
today = datetime.datetime.today()





# Create the calendar
calendar_frame = Frame(root)
calendar_frame.pack(side=LEFT, fill=BOTH, expand=True)
cal = Calendar(calendar_frame, selectmode='day', year=today.year, month=today.month, day=today.day)
cal.pack(pady=20)

# Create the comments section
comments_frame = Frame(root)
comments_frame.pack(side=RIGHT, fill=BOTH, expand=True)

def display_comments():
    comments_list.delete(0, END)
    for date, comment in comments.items():
        comments_list.insert(END, date + ": " + comment)

comments_list = Listbox(comments_frame)
comments_list.pack(fill=BOTH, expand=True)
