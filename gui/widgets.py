from tkinter import *

def create_labeled_entry(parent, label_text, row, column, bg="#f4f4f4"):
    Label(parent, text=label_text, bg=bg, font=("Helvetica", 10)).grid(row=row, column=column, sticky=W, padx=5)
    entry = Entry(parent, width=15)
    entry.grid(row=row+1, column=column, padx=5)
    return entry
