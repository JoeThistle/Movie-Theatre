#Title: Change Movie Data
#Author: Joe Thistlethwaite
#Purpose: To allow for staff to change movie data
#Version: 1.0

from tkinter import *
from tkinter import ttk
import json

with open("Movie Data.json") as file:
    data = json.loads(file.read())

window = Tk()
window.title("Movie Data")
window.geometry("250x275")
window.mainloop()