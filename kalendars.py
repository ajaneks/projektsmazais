import tkinter as tk
from tkinter import ttk
from calendar import monthrange

class Calendar:
    def __init__(self, master):
        self.master = master
        self.master.title("Calendar with Notes")
        
        self.calendar = ttk.Treeview(self.master, selectmode="none")
        self.calendar["columns"] = ("comments")
        self.calendar.column("#0", width=100, minwidth=100)
        self.calendar.column("comments", width=200, minwidth=200)
        self.calendar.heading("#0", text="Date", anchor="center")
        self.calendar.heading("comments", text="Comment", anchor="center")
        
        self.calendar.pack(expand=True, fill="both")
        
        self.calendar.bind("<1>", self.click_date)
        
        self.notes = {}
        self.current_year = 2023
        self.current_month = 2
        
        self.display_month(self.current_year, self.current_month)

    def display_month(self, year, month):
        self.calendar.delete(*self.calendar.get_children())

        num_days = monthrange(year, month)[1]
        for day in range(1, num_days+1):
            date = f"{year}-{month:02d}-{day:02d}"
            if date in self.notes:
                comment = self.notes[date]
            else:
                comment = ""
            self.calendar.insert("", "end", text=date, values=(comment,))

    def click_date(self, event):
        item = self.calendar.identify("item", event.x, event.y)
        date = self.calendar.item(item, "text")

        if date in self.notes:
            comment = self.notes[date]
        else:
            comment = ""

        self.input_window = tk.Toplevel(self.master)
        self.input_window.title("Add Comment")

        tk.Label(self.input_window, text="Comment:").grid(row=0, column=0)
        self.entry = tk.Entry(self.input_window, width=30)
        self.entry.grid(row=0, column=1)
        self.entry.insert(0, comment)

        tk.Button(self.input_window, text="Save", command=lambda: self.save_comment(date)).grid(row=1, column=0, columnspan=2, pady=10)

    def save_comment(self, date):
        comment = self.entry.get()
        self.notes[date] = comment

        if self.calendar.exists(date):
            self.calendar.item(date, values=(comment,))
        else:
            self.calendar.insert("", "end", text=date, values=(comment,))
            
        self.input_window.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    Calendar(root)
    root.mainloop()