#Title: Change Movie Data
#Author: Joe Thistlethwaite
#Purpose: To allow for staff to change movie data
#Version: 1.4

from tkinter import *
from tkinter import ttk
import json

with open("Movie Data.json") as file:
    data = json.loads(file.read())

def showings():
    ''''''
    global movie_selected
    global movies
    movies = data['movies&showings']
    movie_selected = StringVar()
    movie_drop_box = ttk.Combobox(window, textvariable=movie_selected, state="readonly")
    movie_drop_box['values'] = list(movies.keys())
    movie_drop_box.grid(row=2,column=0)
    movie_drop_box.bind("<<ComboboxSelected>>", show_showings)


def show_showings(*args):
    global showings_ent
    try:
        showings_ent.destroy()
    except:
        pass
    num_of_showings = movies[movie_selected.get()]
    showings_ent = Entry(window)
    #I aquired the following line from https://www.geeksforgeeks.org/how-to-set-the-default-text-of-tkinter-entry-widget/
    showings_ent.insert(0, num_of_showings)
    showings_ent.grid(row=2, column=1)
    save_btn = Button(window,text="Save",command=save_showings)
    time_btn.grid_forget()
    save_btn.grid(row=1,column=1)


def save_showings():
    current_movie = movie_selected.get()
    global show_error_lbl
    try:
        current_showings = int(showings_ent.get())
        if current_showings >= 0:
            movies[current_movie] = current_showings
            with open("Movie Data.json","w") as outfile:
                new_data = json.dumps(data,indent=2)
                outfile.write(new_data)
        else:
            try:
                show_error_lbl.grid_remove()
            except:
                pass
            show_error_lbl = Label(window,text="Please Enter A\nPossible Number")
            show_error_lbl.grid(row=3,column=1)
    except:
        try:
                show_error_lbl.grid_remove()
        except:
            pass
        show_error_lbl = Label(window,text="Please Enter A Number")
        show_error_lbl.grid(row=3,column=1)


def back_main():
    '''Goes back to the main menu'''
    for widget in window.winfo_children():
        widget.destroy()
    main_menu()


def time_changer():
    ''''''


def main_menu():
    global time_btn
    main_lbl = Label(window,text="What do you wish to change?")
    showings_btn = Button(window,text="Showings",command=showings)
    time_btn = Button(window,text="Time Slots",command=())
    back_btn = Button(window,text="Back",command=back_main)
    main_lbl.grid(row=0,column=0,columnspan=2)
    time_btn.grid(row=1,column=1)
    showings_btn.grid(row=1,column=0)
    back_btn.grid(row=4,column=0,columnspan=2)
    
window = Tk()
window.title("Movie Data")
window.geometry("300x325")
main_menu()
window.mainloop()